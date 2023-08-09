import sys, getopt
from CWFunctions import performTask

def main(argv):
    user_uuid = ''
    doc_uuid = ''
    task_id = ''
    filename = ''
    
    try:
        options, arguments = getopt.getopt(argv,"u:d:t:f:h:",["userid=","docid=","taskid=","fname=","help="])
    except getopt.GetoptError:
        print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
        sys.exit(2)

    #argument list is segregated according to the predefined list.
    for option, argument in options:
        if option in ("-u", "--userid"):
            user_uuid = argument
        elif option in ("-d", "--docid"):
            doc_uuid = argument
        elif option in ("-t", "--taskid"):
            task_id = argument
        elif option in ("-f", "--fname"):
            filename = argument
        elif option in ("-h", "--help"):
            print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
            sys.exit()
 
    #task ids are validated and verified for corresponding additional requried inputs are passed, based on that data is passed on to the GUI.
    if task_id == '2a':
        if filename=='' or doc_uuid =='':
            print('Filename and Document Id cannot be blank, please enter all the required details.')
            print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
        else:
            performTask('2a', filename, doc_uuid)
    elif task_id == '2b':
        if filename == '' or doc_uuid =='':
            print('Filename and Document Id cannot be blank, please enter all the required details.')
            print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
        else:
            performTask('2b', filename, doc_uuid)
    elif task_id == '3a':
        if filename == '':
            print('Filename cannot be blank, please enter all the required details.')
            print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
        else:
            performTask('3a', filename, doc_uuid)
    elif task_id == '3b':
        if filename == '':
            print('Filename cannot be blank, please enter all the required details.')
            print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
        else:
            performTask('3b', filename, doc_uuid)
    elif task_id == '4':
        if filename == '':
            print('Filename cannot be blank, please enter all the required details.')
            print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
        else:
            performTask('4', filename, doc_uuid)
    elif task_id == '5d':
        if filename == '' or doc_uuid =='':
            print('Filename and Document Id cannot be blank, please enter all the required details.')
            print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
        else:
            performTask('5d', filename, doc_uuid)
    elif task_id == '6':
        if filename == '' or doc_uuid =='':
            print('Filename and Document Id cannot be blank, please enter all the required details.')
            print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
        else:
            performTask('6', filename, doc_uuid)
    elif task_id == '7':
        if filename == '':
            print('Filename cannot be blank, please enter all the required details.')
            print('CW2.py -u <user id> -d <doc id> -t <task id> -f <filename>')
        else:
            performTask('7', filename, doc_uuid)
    else:
        print('No valid task id entered.')

#main function, looks for any Command line arguments, if any process accordingly or directly invoked the GUI.
if __name__ == "__main__":
    if len(sys.argv[1:]) == 0:
        performTask('8','','')
    else:
        main(sys.argv[1:])