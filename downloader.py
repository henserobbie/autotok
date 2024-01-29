import os

FOLDER = 'downloads'

class Downloader:
    def run(downloadQueue, editQueue):
        while True:
            try:
                job = downloadQueue[0]
            except:
                job = None
            if job != None:
                filename = Downloader.download(job)
                editQueue.append({'username': job['username'], 
                                  'id': job['id'], 
                                  'title': job['title'], 
                                  'filename': filename, 
                                  'maxParts':job['maxParts'],
                                  'partLength':job['partLength']})
                downloadQueue.pop(0)
    
    def download(job):
        id = job['id']
        filename = f'{FOLDER}/id{id}.mp4'
        os.system(f"youtube-dl -f 22 -o {filename}  https://www.youtube.com/watch?v={id}")
        return filename