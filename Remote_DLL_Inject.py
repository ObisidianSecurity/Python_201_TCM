from ctypes import *
from ctypes import wintypes

kernel32 = windll.kernel32
LPCTSTR = c_char_P
SIZE_T = c_size_t

OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
OpenProcess.restype = wintypes.HANDLE

VirtualAllocEx = kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = (wintypes.HANDLE, wintypes.LPVOID, SIZE_T, wintypes.DWORD, wintypes.DWORD)
VirtualAllocEx.restype = wintypes.LPVOID

WriteProcessMemory = kernal32.WriteProcessMemory
WriteProcessMemory.argtypes = (wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVoid, SIZE_T, POINTER(SIZE_T))
WriteProcessMemory.restype = wintypes. BOOL

GetModuleHandle = kernel32.GetModuleA
GetModuleHandle,argtypes = (LPCTSTR, )
GetModuleHandle.restype = wintypes.Handle

GetProcAddress =  kernel32.GetProcAddress
GetPrcocAddress.argtypes = (wintypes.HANDLE, LPCTSTR)
GetProcAddress.restype = wintypes.LPVOID

class _SECURITY_ATTRIBUTES(Structure):
    _fields_ = [('nLength', wintypes.DWORD),
                ('lpSecurityDescriptor', wintypes.LPVOID),
               ('bInheritHandle', wintypes.BOOL), ]

SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
LPTHREAD_START_ROUTINE = wintypes.LPVOID

CreateRemoteThread = kernel32.CreateRemoteThread
CreateRemoteThread.argtypes = (wintypes. HANDLE, LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD )
CreateRemoteThread.restype = wintypes.HANDLE

MEM_COMMIT = 0x00001000
MEM_RESERVE = 0x00002000
PAGE_READWRITE = 0x04
EXECUTE_IMMEDIATELY = 0x0
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0x00000FFF)

#dll = Enter the location of the dll here for example b"C:\\Users\\marq\\Documents\\Python201\\hello_world.dll"

pid = 2160

handle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)

if not handle:
    raise WinError()

print("Handle Obtained => {0:X}".format(handle))  

remote_memory = VirtualAllocEx(handle, False, len(dll) + 1, MEM_COMMIT | MEM_RESERVE | PAGE_READWRITE)

if not remote_memory:
    raise WinError()

print("Memory Allocated => {0:X}", hex(remote_memory))

write = WriteProcessMemory(handle, remote_memory, dll, len(dll) + 1, None)

if not write:
    raise WinError()

print("Bytes Written => {}".format(dll))

load_lib = GetProcAddress(GetModuleHandle(b"kernel32.dll") , b"LoadLibraryA")

print("LoadLibrary Address => ", hex(load_lib))

rthread = CreateRemoteThread(handle, None, 0, load_lib, remote_memory, EXECIUR_IMMEDIATELY, None) 
