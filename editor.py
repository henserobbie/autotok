import moviepy.editor as mp
import random
import os
from skimage.filters import gaussian
import pandas

class Editor:
    def run(editQueue, postQueue, accounts):
        while True:
            try:
                job = editQueue[0]
            except:
                job = None
            if job != None:
                i = accounts.index[accounts['username'] == job['username']].tolist()[0]
                secondary = True if accounts['editType'][i] == 2 else False
                result = Editor.edit(job, postQueue, secondary=secondary, addTitle=True)
                if result:
                    editQueue.pop(0)
                else:
                    print('edit failde on edit job: ', job)
                    editQueue.pop(0) #change to not pop if edit fails
                # for result in results:
                #     postJob = {'username': job['username'], 'title': result['title'], 'filename':result['filename']}
                #     postQueue.put(postJob)
    
    def edit(job, postQueue, secondary=False, addTitle=False):
        filename1 = job['filename']
        video_id = job['id']
        title = job['title']
        s = job['partLength']
        maxParts = job['maxParts']
        width = 1280
        try:
            video = mp.VideoFileClip(filename1)
        except:
            return False
        #downsize video if needed
        if video.w > width:
            video.resize(width=width)
        #create intervals
        intervals = Editor.createIntervals(video.duration, s, maxParts)
        #break vid into parts
        for i in range(len(intervals)):
            clip = video.subclip(intervals[i][0], intervals[i][1])
            #get blurred bg clip
            blur = clip.fl_image(Editor.blur)
            x1 = blur.w * (1 - (9**2)/(16**2)) / 2
            x2 = blur.w - x1
            blur = blur.crop(x1=x1, x2=x2, y1=0, y2=blur.h)
            #stack clips
            if secondary:
                clip = mp.clips_array([[clip], [Editor.getSecondary(clip.duration, clip.w)]])
            #cut off sides
            x1 = clip.w / 8
            x2 = clip.w - x1
            clip = clip.crop(x1=x1, x2=x2, y1=0, y2=clip.h)
            #add title
            currTitle = title + ' - Part ' + str(i+1)
            if addTitle:
                txt_clip = mp.TextClip(currTitle, size=(clip.w, clip.w//16), color = 'white', font='Arial-Rounded-MT-Bold').set_duration(clip.duration)
                clip = mp.clips_array([[txt_clip], [clip]])
            #combine with blurred background
            blur = blur.resize(width = clip.w)
            clip = clip.margin(top=(blur.h - clip.h)//2, opacity=0)
            clip = mp.CompositeVideoClip([blur, clip], use_bgclip=True)
            #fix odd pixel bug
            if clip.h % 2 == 1:
                clip = clip.margin(bottom=1)
            if clip.w % 2 == 1:
                clip = clip.margin(right=1)
            new = f"final/id{video_id}_part{i+1}.mp4"
            print('saving: ', new)
            clip.write_videofile(new, preset='ultrafast', fps=24)
            postJob = {
                'username': job['username'],
                'filename': new,
                'title': currTitle,
            }
            postQueue.append(postJob)
        return True
    
    def editFast(job, postQueue, secondary=False, addTitle=False):
        # filename1 = job['filename']
        # video_id = job['id']
        # title = job['title']
        # s = job['partLength']
        # maxParts = job['maxParts']
        # width = 1280
        # try:
        #     video = mp.VideoFileClip(filename1)
        # except:
        #     return False
        # #create intervals
        # intervals = Editor.createIntervals(video.duration, s, maxParts)
        # del video
        # #break vid into parts
        # for i in range(len(intervals)):
        #     #get blurred bg clip
        #     x1 = blur.w * (1 - (9**2)/(16**2)) / 2
        #     x2 = blur.w - x1
        #     #stack clips
            
        #     #cut off sides
            
        #     #add title
        #     currTitle = title + ' - Part ' + str(i+1)
            
        #     #combine with blurred background
            
        #     #fix odd pixel bug
            
        #     new = f"final/{video_id}_part{i+1}.mp4"
        #     postJob = {
        #         'username': job['username'],
        #         'filename': new,
        #         'title': currTitle,
        #     }
        #     postQueue.append(postJob)
        return True
    
    def getSecondary(d, w):
        filename2 = 'secondary/' + random.choice(os.listdir(os.getcwd() + '/secondary'))
        secondary = mp.VideoFileClip(filename2).without_audio().resize(width=w)
        start = random.randint(0, int(secondary.duration - d))
        end = start + d
        secondary = secondary.subclip(start, end)
        return secondary
    
    def createIntervals(d, s, maxParts):
        breaks = [i for i in range(0, int(d), s)]
        breaks.append(d)
        if len(breaks) > 2:
            breaks.pop(-2)
        intervals = []
        for i in range(min(maxParts, len(breaks)-1)):
            intervals.append([breaks[i], breaks[i+1]])
        return intervals

    def blur(image):
        """ Returns a blurred (radius=2 pixels) version of the image """
        return gaussian(image.astype(float), sigma=2)
    
if __name__ == "__main__":
    #fill queue
    editQueue = []
    job = {'username':'south_perks', 
           'filename':'secondary/iddvjy6V4vLlI.mp4', 
           'id':'dvjy6V4vLlI', 
           'title': 'Sample Title Awesomeness', 
           'partLength': 10,
           'maxParts': 1,
           'editType': 2}
    editQueue.append(job)
    postQueue = []
    #get accounts
    accounts = pandas.read_csv('accounts.csv')
    #run
    Editor.run(editQueue, postQueue, accounts)