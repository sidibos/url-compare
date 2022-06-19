
import requests, sys, argparse

def main():
    url1, url2, ifile = process_args()
    #resp = requests.get("https://google.com")
    if ifile != None:
        print("process file")
    else:
        print(f"Url1: {url1}, Url2: {url2}")



def process_args():
    parser = argparse.ArgumentParser(description='Compare two URLs content and metadata values', 
            prog='url_compare')
    parser.add_argument('-i', '--ifile', nargs='?', help='input filename content list of URls')
    parser.add_argument('-o', '--ofile', nargs='?', help='Filename to output the result')
    parser.add_argument('-l1', '--link1', nargs='?', help="First UrL link")
    parser.add_argument('-l2', '--link2', nargs='?', help='Second URL link')

    try:
        args = parser.parse_args()
        
        link1 = args.link1
        link2 = args.link2
        ifile = args.ifile
        ofile = args.ofile

        if (link1 != None or link2 != None) and ifile != None:
            raise Exception("Only one of these two can be provided (link1 and link2) or ifile ")
    except argparse.ArgumentError as e:
        sys.exit(e.message())
    except Exception as e:
        sys.exit(str(e))

    url1 = 'link1'
    url2 = 'link2'

    return url1, url2, ifile

if __name__ == "__main__":
    main()