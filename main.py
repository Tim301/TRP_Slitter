import sys, os, json,subprocess

trp_path = sys.argv[1]
if os.path.isfile(trp_path):
    json_info = subprocess.run(['ffprobe', '-show_programs', '-of', 'json', '-v', 'quiet', '-i', trp_path], stdout=subprocess.PIPE) #Probe trp and pipe results
    json_info = json_info.stdout.decode('utf-8') #Just in case
    trp_info = json.loads(json_info) #Parse json into an object

    #Get all video steam id
    ProgramId = []
    for prg in trp_info['programs']:
        ProgramId.append(str(prg['program_id']))
    print(str(len(ProgramId)) + " programs found")

    print("Start extraction")
    for i, id in enumerate(ProgramId):
        index = "0:p:" + str(id)
        WorkDir = os.getcwd()
        pathout = os.path.splitext(trp_path)[0]  + "_ProgramId_" + id + ".ts" #Must use os.fspath() to convert pathlib type into str
        subprocess.run(['ffmpeg', '-y', '-nostats', '-loglevel', '0', '-i',trp_path, '-c', 'copy', '-map', index, pathout]) #Subprocess only accept str as type path
        if os.path.isfile(pathout):
        	print(str(i+1) + "/" + str(len(ProgramId)) + " programs extraction SUCEED")
        else: 
        	print(str(i+1) + "/" + str(len(ProgramId)) + " programs extraction FAILED")
    print("JOB COMPLETED")
else:
    print("Trp no found")
