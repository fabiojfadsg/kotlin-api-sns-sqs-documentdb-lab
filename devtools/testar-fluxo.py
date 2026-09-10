"""Teste HTTP e reentrega na infraestrutura local; somente dados fictícios."""
import json, time, urllib.request, urllib.error, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def request(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request('http://127.0.0.1:8080'+path, data=data, method=method, headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=20) as res: return res.status, json.load(res)
    except urllib.error.HTTPError as e: return e.code, None
payload = {'nome':'Cliente Teste Local','email':'teste@example.com','cpf':'12345678901'}
assert request('POST','/clientes',dict(payload,cpf='1'))[0] == 400
status, accepted = request('POST','/clientes',payload)
assert status == 202, status
id = accepted['requestId']
for _ in range(30):
    status, saved = request('GET','/clientes/'+id)
    if status == 200: break
    time.sleep(1)
assert status == 200 and saved['cpf'] == payload['cpf'], (status,saved)
compose = ['docker','compose','-f',str(ROOT/'infra/compose.yaml')]
def local(*args):
    return subprocess.check_output(compose+['exec','-T','localstack','awslocal',*args],text=True)
url = json.loads(local('sqs','get-queue-url','--queue-name','cadastro-solicitado'))['QueueUrl']
local('sqs','send-message','--queue-url',url,'--message-body',json.dumps({'requestId':id,'dados':payload}))
time.sleep(5)
count = subprocess.check_output(compose+['exec','-T','mongodb','mongosh','--quiet','cadastro_lab','--eval',f'db.clientes.countDocuments({{_id:"{id}"}})'],text=True).strip()
assert count == '1', count
assert request('POST','/clientes',payload)[0] == 202 # novo pedido, outro ID permitido
print('OK: inválido=400, publicação=202, consumidor persistiu e reentrega manteve um documento. requestId='+id)
