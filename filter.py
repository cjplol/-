'''
指定类别文件夹，遍历每个文件夹中的视频帧，决定是否过滤
空格键：重新播放一次视频帧
回车键：不过滤
F键：过滤该视频帧，并将该视频帧文件夹移动到 filter/类别名 的文件夹中
'''
import os
import cv2 as cv
from shutil import move

#播放视频帧（输入参数：视频帧文件夹路径，类别名）
def handle_video(frames_dir,category):
    frame_list=sorted([os.path.join(frames_dir,f) for f in os.listdir(frames_dir)]) #按顺序排序
    while True:
        FILTER=False  #是否过滤视频
        RESERVE=False #是否保留视频
        #播放视频帧
        for frame in frame_list:
            img=cv.imread(frame)
            img=cv.resize(img,(512,512))
            # 播放当前帧
            cv.imshow(frames_dir, img)
            if cv.waitKey(10) == ord('f'):  #按f键过滤文件到filter/类别名 文件夹中
                FILTER=True
                break
            if cv.waitKey(10) == ord('s'):  #按s键保留文件到reserve/类别名 文件夹中
                RESERVE=True
                break
        if FILTER or RESERVE:
            break
        cv.destroyAllWindows()

    # #保留视频，文件夹移动到reserve/类别名 文件夹中
    # if RESERVE:
    #     target_path=os.path.join('reserve',category)
    #     if not os.path.exists(target_path):
    #         os.makedirs(target_path)
    #     move(frames_dir,target_path)
    #
    # # 过滤视频，文件夹移动到filter/类别名 文件夹中
    # elif FILTER:
    #     target_path = os.path.join('filter', category)
    #     if not os.path.exists(target_path):
    #         os.makedirs(target_path)
    #     move(frames_dir, target_path)

if __name__ == '__main__':
    category="move_body" #对哪个类别进行过滤，文件夹需要以类别命名，类别更换时需要手动更改
    dir_list=os.listdir(category)
    for dir in dir_list:
        dir_path=os.path.join(category,dir)
        handle_video(dir_path,category)