import tkinter as tk
import pickle, pandas
from contentFinder import ContentFinder
from multiprocessing import Process, Manager
from downloader import Downloader
from editor import Editor
from poster import Poster

ACCOUNTS = 'accounts.csv'
BLACKLIST = 'savedata/blacklist.pckl'
DOWNLOADQUEUE = 'savedata/downloadQueue.pckl'
EDITQUEUE = 'savedata/editQueue.pckl'
POSTQUEUE = 'savedata/postQueue.pckl'
MANAGER = 'savedata/manager.pckl'

class Application:
    def __init__(self):
        #create manager
        self.manager = Manager()
        #load in queues
        try:
            f = open(DOWNLOADQUEUE, 'rb')
            self.downloadQueue = self.manager.list(pickle.load(f))
            f.close()
        except:
            print('Cannot find download queue, creating empty queue!')
            self.downloadQueue = self.manager.list()
        try:
            f = open(EDITQUEUE, 'rb')
            self.editQueue = self.manager.list(pickle.load(f))
            f.close()
        except:
            print('Cannot find edit queue, creating empty queue!')
            self.editQueue = self.manager.list()
        try:
            f = open(POSTQUEUE, 'rb')
            self.postQueue = self.manager.list(pickle.load(f))
            f.close()
        except:
            print('Cannot find post queue, creating empty queue!')
            self.postQueue = self.manager.list()
        #load in blacklist
        try:
            f = open(BLACKLIST, 'rb')
            self.blacklist = pickle.load(f)
            f.close()
        except:
            print('Cannot find blacklist, creating empty set!')
            self.blacklist = set()
        #load in accounts
        self.accounts = pandas.read_csv(ACCOUNTS)
        #print start state
        print('Blacklist: ', self.blacklist)
        print('\nDownload Queue: ', self.downloadQueue)
        print('\nEdit Queue: ', self.editQueue)
        print('\nPost Queue: ', self.postQueue)
        #launch backend services
        self.downloader = Process(target = Downloader.run, args=(self.downloadQueue, self.editQueue))
        self.editor = Process(target=Editor.run, args=(self.editQueue, self.postQueue, self.accounts))
        self.poster = Process(target=Poster.run, args=(self.postQueue, self.accounts))
        self.downloader.start()
        self.editor.start()
        self.poster.start()

    def mainWindow(self):
        #main window with status
        window = tk.Tk()
        #button selection for accounts to upload to
        for i in range(self.accounts.shape[0]):
            tk.Button(window, text=f'Get Content for {self.accounts["username"][i]}',\
                       command=lambda i=i: self.getContent(self.accounts['username'][i], self.accounts['search'][i])).pack()
        window.mainloop()
        return
    
    def getContent(self, username, searchterms):
        #fetch video
        content = ContentFinder.query(searchterms, self.blacklist)
        #confirmation window
        root = tk.Tk()
        tk.Label(root, text = f'Found video:\n\
                                Title: {content["title"]}\n\
                                Duration: {content["duration"]}\n\
                                Would you like to use the video? (enter max parts below)').pack()
        tk.Label(root, text='New Title:').pack()
        t = tk.StringVar(root, content['title'])
        tk.Entry(root, textvariable=t).pack()
        tk.Label(root, text='Max Parts:').pack()
        parts = tk.StringVar(root)
        tk.Entry(root, textvariable=parts).pack()
        tk.Label(root, text='Part Length (seconds):').pack()
        partLen = tk.StringVar(root, 60)
        tk.Entry(root, textvariable=partLen).pack()
        def no():
            self.blacklist.add(content['id'])
            root.destroy()
        def yes(t, parts, partLen):
            try:
                maxParts = int(parts.get())
            except:
                maxParts = 5
            try:
                partLength = int(partLen.get())
            except:
                partLength = 60
            downloadJob = {'username':username, 'id':content['id'], 'title':t.get(), 'maxParts':maxParts, 'partLength':partLength}
            print('Added Job to Download Queue: ', downloadJob)
            self.downloadQueue.append(downloadJob)
            root.destroy()
        tk.Button(root, text='no (add to blacklist)', command=no).pack()
        tk.Button(root, text='yes (add to download queue)', command=lambda:yes(t, parts, partLen)).pack()
        root.mainloop()
    
    def __del__(self):
        #terminate processes
        self.downloader.terminate()
        self.editor.terminate()
        self.poster.terminate()
        #save blacklist
        f = open(BLACKLIST, 'wb')
        pickle.dump(self.blacklist, f)
        f.close()
        #save queues
        f = open(DOWNLOADQUEUE, 'wb')
        pickle.dump(list(self.downloadQueue), f)
        f.close()
        f = open(EDITQUEUE, 'wb')
        pickle.dump(list(self.editQueue), f)
        f.close()
        f = open(POSTQUEUE, 'wb')
        pickle.dump(list(self.postQueue), f)
        f.close()
    
if __name__ == "__main__":
    app = Application()
    app.mainWindow()
    del app