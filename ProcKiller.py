'''
1. FindWindowA: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-findwindowa
2. GetWindowThreadProcessId: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid
3. OpenProcess: https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess
4. TerminateProcess: https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess
Include Error Handling
    Will have to be in the form of if|else statements as ctypes doesn't usually throw errors to STDOUT

All variable names are based on the functions parameter names
'''

import ctypes

class ProcKiller():
    def __init__(self):
        # Initializing all the DLLs and constants that will be needed
        self.user_handle = ctypes.WinDLL("User32.dll")
        self.k_handle = ctypes.WinDLL("Kernel32.dll")
        
        # We need to have the flag like this because the base flag is too large
        self.PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
    
    def main(self):
        """
        Main function will do all of the required steps to kill a process in order
        The naming conventions of the variables used in this function will reflect the 
        parameters that need to be passed to the next function
        """
        hWnd = self.findWindowName()
        lpdwProcessId = self.getProcId(hWnd)
        hProcess = self.getHandle(lpdwProcessId)
        self.terminateProcess(hProcess)
        
        
    def findWindowName(self):
        """
        This function will return the handle to the window we specify
        """
        # Setting up parameters for the FindowWindowA function (Takes a pointer of the window name)
        lpWindowName = ctypes.c_char_p(input("Type window name to kill: ").encode("utf-8"))

        # Catching response of the function and setting up the error handling
        hWnd = self.user_handle.FindWindowA(None, lpWindowName)

        if hWnd == 0:
            print("Couldn't create handle to process/window name entered. Error Code: {}".format(self.k_handle.GetLastError()))
            exit(1)
        else:
            print("Created Handle: {}".format(hWnd))
            return hWnd

    def getProcId(self, hWnd):
        """
        This function will get the Process ID of the window we got the handle of
        """
        # Initializing a variable with type DWORD
        lpdwProcessId = ctypes.c_ulong()

        # Getting the threads Process ID and the return output will go into the reference of the DWORD variable
        response = self.user_handle.GetWindowThreadProcessId(hWnd, ctypes.byref(lpdwProcessId))

        if response == 0:
            print("Could not grab PID. Error Code: {}".format(self.k_handle.GetLastError()))
            exit(1)
        else:
            print("Got PID: {}".format(response))
            return lpdwProcessId
    
    def getHandle(self, lpdwProcessId):
        """
        This function serves to open an existing local process object with certain privileges
        """
        # This will determine what access rights we desire
        wdDesiredAccess = self.PROCESS_ALL_ACCESS
        # If we have any processes spawned off of this one, do we want them to inherit the same handle?
        bInheritHandle = False
        # The identifier of the local process to be opened being the PID
        dwProcessId = lpdwProcessId

        hProcess = self.k_handle.OpenProcess(wdDesiredAccess, bInheritHandle, dwProcessId)

        if hProcess <= 0:
            print("Could not grab Privileged Handle. Error Code: {}".format(self.k_handle.GetLastError()))
            exit(1)
        else:
            print("Got Privileged Handle: {}".format(hProcess))
            return hProcess

    def terminateProcess(self, hProcess):
        """
        This function serves to terminate the process by the TerminateProcess function
        """
        
        # Using 1 as its the default return code for error
        uExitCode = 0x1

        response = self.k_handle.TerminateProcess(hProcess, uExitCode)
        
        if response <= 0:
            print("Process did not terminate. Error Code: {}".format(self.k_handle.GetLastError()))
        else:
            print("Process Terminated")

if __name__ == '__main__':
    pk = ProcKiller()
    pk.main()