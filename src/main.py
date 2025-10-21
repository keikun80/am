import amcollector
import time 
import os
from multiprocessing import Process
import signal
from lib import amconfig

def start_processes(items):
    """설정 아이템 목록을 기반으로 자식 프로세스를 시작합니다."""
    processes = []
    for item in items:
        try:
            obj = amcollector.Am(item)
            p = Process(target=obj.toRequest, args=())
            p.start()
            processes.append(p)
            print(f"Started process for '{item['name']}' (PID: {p.pid})")
        except KeyError as e:
            print(f"Error: Missing key {e} in configuration item: {item}. Skipping.")
    return processes

def stop_processes(processes):
    """실행 중인 모든 자식 프로세스를 종료합니다."""
    for p in processes:
        if p.is_alive():
            p.terminate() # SIGTERM 전송
            p.join(timeout=5) # 프로세스가 종료될 때까지 최대 5초 대기
            if p.is_alive():
                p.kill() # 5초 후에도 살아있으면 강제 종료 (SIGKILL)
            print(f"Stopped process (PID: {p.pid})")

if __name__ == "__main__":
    last_mtime = 0
    running_processes = []
    
    # 시그널 핸들러 설정
    def signal_handler(signum, frame):
        """SIGINT와 SIGTERM 시그널을 처리하여 프로세스를 안전하게 종료합니다."""
        print(f"\nSignal {signum} received. Shutting down all processes...")
        stop_processes(running_processes)
        # 자식 프로세스들이 모두 종료된 후, 메인 프로세스를 종료합니다.
        # 이 예제에서는 while 루프가 자연스럽게 종료되도록 break를 사용하지 않고,
        # 루프 조건을 변경하거나 직접 종료할 수 있습니다.
        # 여기서는 KeyboardInterrupt를 다시 발생시켜 기존 로직을 활용합니다.
        raise KeyboardInterrupt
    
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C 처리
    signal.signal(signal.SIGTERM, signal_handler) # 종료 시그널 처리
    
    while True:
        try:
            current_mtime = os.path.getmtime(amconfig.configFile)
            if current_mtime != last_mtime:
                print("Configuration file changed. Reloading processes...")
                stop_processes(running_processes)
                items = amconfig.get_items()
                running_processes = start_processes(items)
                last_mtime = current_mtime
            time.sleep(10)  # 10초마다 설정 파일 변경 확인
        except KeyboardInterrupt:
            # signal_handler 또는 직접적인 Ctrl+C에 의해 실행됩니다.
            print("Exiting main program.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            stop_processes(running_processes)
            break