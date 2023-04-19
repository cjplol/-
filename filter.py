'''
指定类别文件夹，遍历每个文件夹中的视频帧，决定是否过滤
F键：过滤该视频帧，并将该视频帧文件夹移动到 filter/类别名 的文件夹中
S键：保留该视频帧，并将该视频帧文件夹移动到 reserve/类别名 的文件夹中
C键：返回上一个视频帧，并重新处理
'''
import os
import cv2 as cv
from shutil import move
import paramiko

# 设定远程服务器的IP地址、用户名和密码
host = '192.168.1.226'
# port = 22
username = 'kinth'
password = 'qs@123456'
base_path = os.getcwd()
# 创建SSH客户端对象
ssh = paramiko.SSHClient()

# 自动添加缺失的主机密钥
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接到远程服务器
ssh.connect(host, username=username, password=password)
# 类别文件夹在服务器的路径
server_img_dir_path = '/home/kinth/mfq/PaddleVideo/data/invigilator/all_frames_half/hands_down'
# 在服务器中过滤到哪个文件夹
server_img_dir_outpath = '/home/kinth/mfq/PaddleVideo/data/invigilator/filter/hands_down'

#播放视频帧（输入参数：视频帧文件夹路径，上一个视频路径，上一个视频是否过滤，上一个视频是否保留）
def handle_video(frames_dir,last_path,last_filter,last_reserve):
    frame_list=sorted([os.path.join(frames_dir,f) for f in os.listdir(frames_dir)]) #按顺序排序
    dir_name_path=os.path.dirname(frames_dir) #处理视频帧的文件夹的相对路径
    frames_name=frames_dir.split('\\')[-1]
    server_img_path = server_img_dir_path+"/"+frames_name  # 服务器中视频帧文件夹名
    while True:
        FILTER=False  #是否过滤视频
        RESERVE=False #是否保留视频
        #播放视频帧
        for frame in frame_list:
            img=cv.imread(frame)
            img=cv.resize(img,(512,512))
            # 播放当前帧
            cv.imshow(frames_dir, img)
            key=cv.waitKey(20)
            if key == ord('f'):  #按f键过滤文件到filter/类别名 文件夹中
                FILTER=True
                break
            elif key == ord('s'):  #按s键保留文件到reserve/类别名 文件夹中
                RESERVE=True
                break
            elif key == ord('c'):  # 按c键返回上一个视频帧，并重新处理
                if last_path=='' or (last_filter==False and last_reserve==False):
                    continue
                else:
                    cv.destroyAllWindows()
                    if last_filter:
                        src_path=os.path.join('filter',last_path) #上一个文件的路径
                        target_path=dir_name_path    #原路径
                        move(src_path,target_path)   #移动回原路径
                        handle_video(last_path,'',False,False) #重新处理

                    if last_reserve:
                        src_path = os.path.join('reserve',last_path) #上一个文件的路径
                        target_path = dir_name_path #原路径
                        move(src_path, target_path) #移动回原路径
                        handle_video(last_path, '', False, False)#重新处理

        if FILTER or RESERVE:
            break
    cv.destroyAllWindows()

    #保留视频，文件夹移动到reserve/类别名 文件夹中
    if RESERVE:
        target_path=os.path.join('reserve',category)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        move(frames_dir,target_path)

    # 过滤视频，文件夹移动到filter/类别名 文件夹中
    elif FILTER:
        target_path = os.path.join('filter', category)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        move(frames_dir, target_path)

        # 执行移动文件命令
        ssh.exec_command(f'mv {server_img_path} {server_img_dir_outpath}')  # 在服务器中进行文件夹移动

    return FILTER,RESERVE

if __name__ == '__main__':

    category="hands_down" #对哪个类别进行过滤，文件夹需要以类别命名，类别更换时需要手动更改
    dir_list=os.listdir(category)
    last_path='' #记录上一个视频帧的文件夹路径，防止误处理
    last_filter=last_reserve=False
    for dir in dir_list:
        dir_path=os.path.join(category,dir)
        last_filter,last_reserve=handle_video(dir_path,last_path,last_filter,last_reserve)
        last_path=dir_path
