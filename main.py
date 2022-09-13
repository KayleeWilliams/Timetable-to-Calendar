import scrape2
import new_google
import time


def main():
    st = time.time()
    res = scrape2.main()
    print(time.time() - st)
    if (len(res[0]) > 0) or (len(res[1]) > 0):
        new_google.main(res[0], res[1])
        print(time.time() - st)

if __name__ == "__main__":
    main()
