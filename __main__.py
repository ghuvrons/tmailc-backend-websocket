import PySan

if __name__ == "__main__":
    try:
        pySan = PySan.PySan()
        pySan.addVHost({'localhost': 'localhost'})
        pySan.start()
    except KeyboardInterrupt:
        print("closing")
        pySan.close()