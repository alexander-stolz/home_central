import sonoff, time

s = sonoff.Sonoff('amstolz@gmail.com', R'Ewelink\3193*', 'eu')
devices = s.get_devices()
for d in devices:
    name = d.get('name')
    print(name)
    s.switch('off', d.get('deviceid'))
    time.sleep(1)
