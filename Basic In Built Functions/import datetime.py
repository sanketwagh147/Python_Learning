from datetime import datetime
current_time = datetime.now()
print(":".join([str(current_time.hour),str(current_time.minute), str(current_time.second)]))
