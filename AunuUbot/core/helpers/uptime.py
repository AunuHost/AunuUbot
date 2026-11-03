from time import time as waktunya

start_time = waktunya()


async def get_time(seconds):
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "\u1d0d", "\u029c", "\u1d05"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        elif count == 3:
            remainder, result = divmod(seconds, 24)
        else:
            # count == 4: seconds is now in days, no further division needed
            remainder = 0
            result = seconds
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        up_time += time_list.pop() + ":"

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time
