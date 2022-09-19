import re
import json
import sys 
import pathlib 
import os 

md_table = """ 
<!--- API Define -->
<!--- File:test1.json -->
| key        | Some Description             | testcase    |
|------------|------------------------------|-------------|
| Dark Souls | This is a fun game           | 5           |
| Bloodborne | This one is even better      | 2           |
| Sekiro     | This one is also pretty good | 110101      |



<!--- API Define -->
<!--- File:test2.json -->
| key        | Some Description             | testcase    |
|------------|------------------------------|-------------|
| Dark Souls | This is a fun game           | 5           |
| Bloodborne | This one is even better      | 2           |
| Sekiro     | This one is also pretty good | 110101      |
"""

KEY_NAME = "key"
TEST_NAME = "testcase"

def table_tojson(inputstr):
  lines = inputstr.split('\n')
  ret={}
  keyindex = 0
  testindex = 2
  keyindex,testindex,filename,dlines = checkAttribute(lines) 
  #print(filename)
  #print(dlines)
  for i,l in enumerate(dlines):
    for _i,v in enumerate(l.split('|')): 
      if _i == keyindex : key = v.strip() 
      if _i == testindex : test = v.strip()
    ret[key] = test
  if len(filename) > 0 :
    os.makedirs("output",exist_ok=True)
    p = pathlib.Path("output",filename)
    with p.open(mode="w") as f:
      json.dump(ret,f,indent=2)
  return json.dumps(ret, indent = 2) 

def checkAttribute(lines):
  filename=""
  testindex=-1
  keyindex=-1
  comment=False
  dataindex= 0
  for i,l in enumerate(lines):
    if "File:" in l : 
      filename = l[l.index("File:")+5:l.rindex(".json")+5] 
      print(l)
    elif "key" in l :
      keys=[_i.strip() for _i in l.split('|')]
      keyindex = keys.index(KEY_NAME)
      testindex = keys.index(TEST_NAME)
    elif "---" in l :
      comment = True 
    else :
      dataindex = i
      break
  return keyindex,testindex,filename,lines[dataindex:]

def mrkdtojson(stream) :
  pattern = re.compile(r'<!--- API Define -->.+?\n$',re.MULTILINE | re.DOTALL)
  l = []
  for match in pattern.finditer(stream):
    table =match.group(0).replace(r'<!--- API Define -->','')[1:]
    json = table_tojson(table) 
    print(json)
   

if __name__ == '__main__':
  with open(sys.argv[1],"r") as f:
    content = f.read()
    mrkdtojson(content)
