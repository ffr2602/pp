import roslibpy
import numpy as np
import time 

class Monitoring:
    def __init__(self):
        self.client = roslibpy.Ros(host='localhost', port=9090)
        self.position_sub = roslibpy.Topic(self.client, '/odom', 'nav_msgs/Odometry')
        self.reff_dat_sub = roslibpy.Topic(self.client, '/odom_ref', 'nav_msgs/Odometry')
        self.kondisi = roslibpy.Topic(self.client, '/robot_kondisi', 'std_msgs/String')

        self.position = np.zeros(3).astype(float)
        self.position_ref = np.zeros(3).astype(float)
        self.kondisi_data_ = ''

    def Position_data(self, msg):
        self.position[0] = msg['pose']['pose']['position']['x']
        self.position[1] = msg['pose']['pose']['position']['y']
        self.position[2] = msg['pose']['pose']['orientation']['w']
    
    def Odom_ref(self, msg):
        self.position_ref[0] = msg['pose']['pose']['position']['x']
        self.position_ref[1] = msg['pose']['pose']['position']['y']
        self.position_ref[2] = msg['pose']['pose']['orientation']['w'] 
    
    def data_kondisi(self, msg):
        self.kondisi_data_ = msg['data']


def main():
    monitor = Monitoring()
    try:
        monitor.client.run()
        while True:
            monitor.position_sub.subscribe(monitor.Position_data)
            monitor.reff_dat_sub.subscribe(monitor.Odom_ref)
            monitor.kondisi.subscribe(monitor.data_kondisi)
            if monitor.kondisi_data_ == 'OnTrack':
                file = open('data.txt', 'a')
                data = '{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n'.format(monitor.position[0], monitor.position_ref[0], monitor.position[1], monitor.position_ref[1])
                print(data)
                file.write(data)
                file.close()
                print("jalan")
            else:
                print("stop")
    except KeyboardInterrupt:
       file.close()
       monitor.client.terminate()

if __name__ == '__main__':
    main()
