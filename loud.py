import glob
import multiprocessing
from multiprocessing import Process, Queue
from multiprocessing import Queue
import glob,subprocess,traceback

def f(x):
    return x*x

def yy(q:Queue):
    if q.empty():
        return
    try:
        i=q.get()
        p = multiprocessing.current_process()
        print(f'pname:{p.name},processing :{i}')
        subprocess.run(["ffmpeg","-i",i,"-af","volume=6",f'{i[:-4]}-loud.mp3'])
    except:
        print(f'pname:{p.name},error')
        print(traceback.format_exc())

if __name__ == "__main__":
    q=Queue()
    files=glob.glob("*.mp3")
    for i in files:
        q.put(i)
    while not q.empty():
        plist=[]
        for _ in range(multiprocessing.cpu_count()-1):
            plist.append(Process(target=yy,args=(q,)))
        for i in plist:
            i.start()
        for i in plist:
            i.join()


def xx():
    a=glob.glob("*.mp3")
    for i in a:
        print(i)
    # subprocess.run(["chmod","+x",f"{os.path.join(os.path.abspath('.'),'getmp3list.sh')}"])
