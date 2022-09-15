import scrape
import google_calendar
import time


def main():
    st = time.time()
    res = scrape.main()
    print(time.time() - st)
    if (len(res[0]) > 0) or (len(res[1]) > 0):
        st = time.time()
        google_calendar.main(res[0], res[1])
        print(time.time() - st)

if __name__ == "__main__":
    main()
