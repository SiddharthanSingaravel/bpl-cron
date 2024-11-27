import subprocess

def fetchData():
    subprocess.run(["python", "fetchData.py"], check=True)

def runCode():
    subprocess.run(["python", "runCode.py"], check=True)

if __name__ == "__main__":
    fetchData()
    runCode()