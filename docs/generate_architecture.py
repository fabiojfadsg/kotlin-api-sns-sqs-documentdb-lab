"""Gera SVG e draw.io usando os ícones AWS locais (somente biblioteca padrão)."""
from pathlib import Path
import base64
from html import escape
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1560" height="780" viewBox="0 0 1560 780" role="img" aria-labelledby="title desc">',
         '<title id="title">Cadastro assíncrono de clientes</title>',
         '<desc id="desc">Angular envia POST /clients à API Kotlin, que publica no SNS. SQS entrega ao worker, que grava no DocumentDB. Falhas repetidas seguem para uma DLQ.</desc>',
         '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#526174"/></marker></defs>',
         '<rect width="1560" height="780" fill="#ffffff"/>']
doc = ET.Element('mxfile', host='app.diagrams.net')
diagram = ET.SubElement(doc, 'diagram', name='Cadastro de clientes', id='clients')
model = ET.SubElement(diagram, 'mxGraphModel', page='1', pageWidth='1560', pageHeight='780', grid='1', gridSize='10')
root = ET.SubElement(model, 'root')
ET.SubElement(root, 'mxCell', id='0')
ET.SubElement(root, 'mxCell', id='1', parent='0')
counter = 1


def cell(value, style, x, y, w, h):
    global counter
    counter += 1
    c = ET.SubElement(root, 'mxCell', id=str(counter), value=value, style=style, vertex='1', parent='1')
    ET.SubElement(c, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as': 'geometry'})
    return c


def rect(x, y, w, h, fill='#f8fafc', stroke='#cbd5e1', dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{dash}/>')
    cell('', f'rounded=1;arcSize=8;fillColor={fill};strokeColor={stroke};dashed={int(dashed)};', x, y, w, h)


def text(x, y, value, size=16, color='#172b4d', bold=False, center=False):
    anchor = 'middle' if center else 'start'
    parts.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(value)}</text>')
    width = max(100, len(value) * size * .63)
    cell(value, f'text;html=0;align={"center" if center else "left"};verticalAlign=middle;whiteSpace=wrap;fillColor=none;strokeColor=none;fontFamily=Arial;fontSize={size};fontColor={color};fontStyle={int(bold)};', x-width/2 if center else x, y-size, width, size+8)


def icon(name, x, y):
    raw = (HERE / 'assets' / 'aws' / name).read_bytes()
    encoded = base64.b64encode(raw).decode()
    parts.append(f'<image x="{x}" y="{y}" width="64" height="64" href="data:image/svg+xml;base64,{encoded}"/>')
    cell('', f'shape=image;imageAspect=0;aspect=fixed;image=data:image/svg+xml,{encoded};', x, y, 64, 64)


def arrow(points, dashed=False):
    dash = ' stroke-dasharray="6 5"' if dashed else ''
    coords = ' '.join(f'{x},{y}' for x, y in points)
    parts.append(f'<polyline points="{coords}" fill="none" stroke="#526174" stroke-width="2" marker-end="url(#arrow)"{dash}/>')
    global counter
    counter += 1
    c = ET.SubElement(root, 'mxCell', id=str(counter), style=f'edgeStyle=none;endArrow=block;endFill=1;strokeColor=#526174;strokeWidth=2;dashed={int(dashed)};', edge='1', parent='1')
    g = ET.SubElement(c, 'mxGeometry', relative='1', **{'as': 'geometry'})
    for label, point in [('sourcePoint', points[0]), ('targetPoint', points[-1])]:
        ET.SubElement(g, 'mxPoint', x=str(point[0]), y=str(point[1]), **{'as': label})
    if len(points) > 2:
        arr = ET.SubElement(g, 'Array', **{'as': 'points'})
        for x, y in points[1:-1]:
            ET.SubElement(arr, 'mxPoint', x=str(x), y=str(y))


text(40, 52, 'Cadastro de clientes', 30, bold=True)
text(40, 84, 'Arquitetura lógica proposta • Angular + Kotlin + serviços AWS', 17, '#526174')
rect(630, 135, 890, 520, '#ffffff', '#8795a8', True)
text(652, 166, 'Serviços AWS', 18, bold=True)
text(652, 191, 'Agrupamento lógico • não representa VPC ou sub-redes', 13, '#526174')

rect(40, 240, 240, 195)
text(160, 275, 'Angular', 22, bold=True, center=True)
text(160, 308, 'Cadastro de cliente', 16, center=True)
for y, label in [(342, 'Nome'), (375, 'E-mail'), (408, 'CPF')]:
    rect(62, y-20, 196, 27, '#ffffff')
    text(74, y, label, 14, '#526174')
rect(390, 255, 190, 155)
text(485, 298, 'API Kotlin', 21, bold=True, center=True)
text(485, 332, 'Valida a solicitação', 14, center=True)
text(485, 357, 'Publica no SNS', 14, center=True)

for filename, x, title, subtitle in [
    ('sns.svg', 682, 'Amazon SNS', 'Tópico de criação'),
    ('sqs.svg', 932, 'Amazon SQS', 'Fila de criação'),
    ('documentdb.svg', 1352, 'Amazon DocumentDB', 'Coleção de clientes'),
    ('sqs.svg', 932, 'Amazon SQS · DLQ', 'Mensagens com falha')]:
    y = 502 if 'DLQ' in title else 260
    icon(filename, x, y)
    text(x+32, y+92, title, 17, bold=True, center=True)
    text(x+32, y+119, subtitle, 14, '#526174', center=True)

rect(1090, 245, 180, 165, '#f8fafc')
text(1180, 288, 'Worker Kotlin', 20, bold=True, center=True)
text(1180, 323, 'Consome a fila', 14, center=True)
text(1180, 349, 'Persiste o cliente', 14, center=True)
text(1180, 375, 'Confirma após gravar', 13, '#526174', center=True)

arrow([(280, 295), (390, 295)])
text(335, 271, 'POST /clients', 13, center=True)
arrow([(390, 395), (280, 395)], True)
text(335, 427, '202 Accepted', 13, center=True)
arrow([(580, 292), (680, 292)])
text(630, 267, 'Publicação', 13, center=True)
arrow([(748, 292), (930, 292)])
text(839, 267, 'Assinatura do tópico', 13, center=True)
arrow([(996, 292), (1090, 292)])
text(1043, 233, 'Consumo', 13, center=True)
arrow([(1270, 292), (1350, 292)])
text(1310, 233, 'Gravação', 13, center=True)
arrow([(964, 393), (964, 500)], True)
text(986, 451, 'Limite de tentativas', 13)
text(986, 473, 'de processamento excedido', 13)

text(40, 506, 'Resposta ao formulário', 17, bold=True)
text(40, 535, '“Solicitação de cadastro recebida”', 16)
text(40, 563, '202 indica aceite após publicação no SNS.', 14, '#526174')
text(40, 587, 'O cadastro é concluído pelo worker.', 14, '#526174')
text(40, 701, 'API e worker: hospedagem a definir. Posição dos componentes indica apenas o fluxo lógico.', 14, '#526174')
text(40, 730, 'Ícones: AWS Architecture Icons • pacote 31/07/2026. Fluxo assíncrono ainda sujeito à confirmação.', 14, '#526174')
parts.append('</svg>')
(HERE / 'arquitetura.svg').write_text('\n'.join(parts), encoding='utf-8')
ET.indent(doc)
ET.ElementTree(doc).write(HERE / 'arquitetura.drawio', encoding='utf-8', xml_declaration=True)
print('Gerados: docs/arquitetura.svg e docs/arquitetura.drawio')
