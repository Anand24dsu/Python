import requests,json
def Bulid(url):
    response = requests.get(url)
    response.raise_for_status() 

    data = response.json()
    print(data)
    for i in data:
        print(i)
    bulid_data=data["builds"]
    print(bulid_data,end=" ")
    print()
    
    for j in data["builds"]:
        print(j["number"])
        print(j["url"])
    # return url
url="http://localhost:8080/job/MY_FIRST_JOB_WITH_GIT/api/json?pretty=true"
r=Bulid(url)

print(r)    

