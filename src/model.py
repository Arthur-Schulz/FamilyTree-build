import json,os,collections,sys
BUNDLE=os.environ.get('BUNDLE','work/bundle1.json')
J=json.load(open(BUNDLE,encoding='utf-8'))
P=J['people']; U=J['unions']
ARTHUR='arthur-schulz-robellaz'; CONST='constance-fichet'; VERNAGE='marie-louise-vernage-1741'
