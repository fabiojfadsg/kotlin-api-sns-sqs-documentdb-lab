#!/bin/bash
set -euo pipefail
TOPIC=$(awslocal sns create-topic --name cadastro-solicitado --query TopicArn --output text)
DLQ=$(awslocal sqs create-queue --queue-name cadastro-dlq --query QueueUrl --output text)
DLQ_ARN=$(awslocal sqs get-queue-attributes --queue-url "$DLQ" --attribute-names QueueArn --query Attributes.QueueArn --output text)
QUEUE=$(awslocal sqs create-queue --queue-name cadastro-solicitado --query QueueUrl --output text)
ARN=$(awslocal sqs get-queue-attributes --queue-url "$QUEUE" --attribute-names QueueArn --query Attributes.QueueArn --output text)
python3 - "$DLQ_ARN" "$ARN" "$TOPIC" <<'JSON'
import json,sys
json.dump({'RedrivePolicy':json.dumps({'deadLetterTargetArn':sys.argv[1],'maxReceiveCount':'3'}),'Policy':json.dumps({'Version':'2012-10-17','Statement':[{'Effect':'Allow','Principal':{'Service':'sns.amazonaws.com'},'Action':'sqs:SendMessage','Resource':sys.argv[2],'Condition':{'ArnEquals':{'aws:SourceArn':sys.argv[3]}}}]})},open('/tmp/queue-attributes.json','w'))
JSON
awslocal sqs set-queue-attributes --queue-url "$QUEUE" --attributes file:///tmp/queue-attributes.json
awslocal sns subscribe --topic-arn "$TOPIC" --protocol sqs --notification-endpoint "$ARN" --attributes RawMessageDelivery=true
touch /tmp/cadastro-ready
