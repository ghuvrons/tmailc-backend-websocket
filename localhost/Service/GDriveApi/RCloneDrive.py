from rclone import RClone
import subprocess
import tempfile

cfg_temp = """[remote]
type = drive
scope = drive
token = {}
root_folder_id = {}"""

class RCloneDrive(RClone):
    def __init__(self, token, root_folder_id = None):
        self.token = token
        self.root_folder_id = root_folder_id
        if self.root_folder_id:
            cfg = cfg_temp.format(self.token, self.root_folder_id)
            RClone.__init__(self, cfg)
    def onSizeTf(self, transferred, maxSized, progress):
        print("size",  transferred, maxSized, progress)
    def onNumTf(self, transferred, maxSized, progress):
        print("num",  transferred, maxSized, progress)
    def onError(self, message):
        print("error", message)
    def decodeSizeTf(self, msg):
        msg = msg.replace("\n", "").replace(" ", "")
        msg = msg.split(",")
        transferred, maxSized = msg[0].split("/", 1)
        progress = msg[1].replace("%", "")
        if progress != "-":
            self.onSizeTf(transferred, maxSized, progress)

    def decodeNumTf(self, msg):
        msg = msg.replace("\n", "").replace(" ", "")
        msg = msg.split(",")
        transferred, maxSized = msg[0].split("/", 1)
        progress = msg[1].replace("%", "")
        if progress != "-":
            self.onNumTf(transferred, maxSized, progress)

    def _execute(self, command_with_args):
        self.log.debug("Invoking : %s", " ".join(command_with_args))
        
        sizedTransferSplit = "Transferred:   \t  "
        numTransferSplit = "Transferred:           "
        
        try:
            with subprocess.Popen(
                    command_with_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE) as proc:
                # (out, err) = proc.communicate()
                out = b''
                err = b''
                #out = proc.stdout.read()
                line = proc.stdout.readline()
                #err = proc.stderr.read()
                while line:
                    msg = line.decode("utf-8")
                    szTfMsg = msg.split(sizedTransferSplit, 1)
                    numTfMsg = msg.split(numTransferSplit, 1)
                    errorMsg = msg.split("ERROR : ", 1)
                    if len(szTfMsg) > 1:
                        self.decodeSizeTf(szTfMsg[1])
                    if len(numTfMsg) > 1:
                        self.decodeNumTf(numTfMsg[1])
                    if len(errorMsg) > 1:
                        self.onError(errorMsg[1])

                    line = proc.stdout.readline()
                    
                # self.log.debug(out)
                if err:
                    self.log.warning(err.decode("utf-8").replace("\\n", "\n"))

                return {
                    "code": proc.returncode,
                    "out": out,
                    "error": err
                }
        except FileNotFoundError as not_found_e:
            self.log.error("Executable not found. %s", not_found_e)
            return {
                "code": -20,
                "error": not_found_e
            }
        except Exception as generic_e:
            self.log.error("Error running command. Reason: %s", generic_e)
            return {
                "code": -30,
                "error": generic_e
            }

    def copy(self, root_folder_id, dest):
        if root_folder_id:
            cfg = cfg_temp.format(self.token, root_folder_id)
            RClone.__init__(self, cfg)
        return RClone.copy(self, "remote:/", dest, flags=["-P", "--retries", "1"])