import io
import os
import re

#Any unnecessarily qualified object instance is marked.  See
#   http://stackoverflow.com/questions/29293136/compiler-warning-for-unnecessary-namespaces

#Requires CPIP (http://cpip.sourceforge.net/index.html)
try:
    #To install, do not use the setup.py script; it is broken.  Instead, just copy the "cpip" folder
    #   into "[python]/Lib/site-packages/".
    from cpip.core import CppDiagnostic
    from cpip.core import IncludeHandler
    from cpip.core import PpLexer
    from cpip.core import PragmaHandler
    CPIP_available = True
except:
    CPIP_available = False
    print("Skipping unnecessary qualification rule; CPIP not available!  See this rule for installation instructions.")


class RuleUnnecessaryQualification(object):
    NAME = "Unnecessary Qualification"
    
    @staticmethod
    def get_description(line_numbers):
        result = "Unecessary qualification on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        if not CPIP_available: return []
        if not (\
            path.endswith(".h") or\
            path.endswith(".hpp") or\
            path.endswith(".c") or\
            path.endswith(".cc") or\
            path.endswith(".cpp") or\
            path.endswith(".cxx")\
        ): return [] #Can only operate on C/C++ files

        print("Processing: \""+path+"\"!")

        #This version takes forever, is Windows-specific, and has problems for a variety of reasons
##        #Set up lexer
##        #   Includes
##        includes = IncludeHandler.CppIncludeStdOs(
##            theUsrDirs=[],
##            theSysDirs=[
##                #"C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/include",
##                #"C:/Program Files (x86)/Microsoft Visual Studio 10.0/VC/include",
##                #"C:/Program Files (x86)/Microsoft Visual Studio 11.0/VC/include",
##                "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/include",
##                #"C:/Program Files (x86)/Microsoft SDKs/Windows/v7.0A/Include"
##                #"C:/Program Files (x86)/Microsoft SDKs/Windows/v7.1A/Include"
##                #"C:/Program Files (x86)/Windows Kits/8.0/Include/um"
##                "C:/Program Files (x86)/Windows Kits/8.1/Include/um"
##                #"C:/Program Files (x86)/Windows Phone Kits/8.1/Include"
##                #"C:/Program Files (x86)/Windows Phone Silverlight Kits/8.1/Include"
##            ]
##        )
##        #   Pragmas (doesn't understand "#pragma once")
##        pragma = PragmaHandler.PragmaHandlerNull()
##        #   Standard defines (change to suit)
##        #       From http://cpip.sourceforge.net/tutorial/PpLexer.html#advanced-pplexer-construction
##        defines = [
##            #https://msdn.microsoft.com/en-us/library/b0084kay.aspx
##            #Also, "WINAPI_FAMILY", apparently
##            "_WIN32", "__STDC_WANT_SECURE_LIB__=1", "_MFC_VER=0x0800",
##            "_UNICODE","UNICODE"
##        ]
##        def load_file_as_string(path):
##            file = open(path)
##            data = file.readlines()
##            file.close()
##            return u"".join(data)
##        pre_incl = [io.StringIO(load_file_as_string( #Note cannot use io.FileIO, since CPIP crashes at \r.
##            #"C:/Program Files (x86)/Windows Kits/8.0/Include/shared/winapifamily.h"
##            "C:/Program Files (x86)/Windows Kits/8.1/Include/shared/winapifamily.h"
##            #"C:/Program Files (x86)/Windows Phone Kits/8.1/Include/winapifamily.h"
##            #"C:/Program Files (x86)/Windows Phone Silverlight Kits/8.1/Include/winapifamily.h"
##        )),io.StringIO(u"\n".join([u"#define "+u" ".join(d.split("=")) for d in defines])+u"\n")]
##        #   Diagnostic
##        diag = CppDiagnostic.PreprocessDiagnosticKeepGoing()
##        #   Construct lexer
##        #       cpip/core/PpLexer.py:204
##        lexer = PpLexer.PpLexer(path,includes,pre_incl,diag,pragma,None,None)

        #This version is simpler and wrong: it ignores all lower-level headers.  This is good enough for
        #   checking for unnecessary qualification within a program's namespace, though.
        #Set up lexer
        #   Construct lexer
        #       cpip/core/PpLexer.py:204
        class PreprocessDiagnosticCustom(CppDiagnostic.PreprocessDiagnosticStd):
            def undefined(self, msg, theLoc=None): pass
            def error(self, msg, theLoc=None): pass
            def warning(self, msg, theLoc=None): pass
        lexer = PpLexer.PpLexer(
            path,
            IncludeHandler.CppIncludeStdOs([],[]),
            None,
            PreprocessDiagnosticCustom(),
            PragmaHandler.PragmaHandlerNull(), #CPIP doesn't understand, in particular, "#pragma once"
            None,
            None
        )

        tokens = []
        for token in lexer.ppTokens(minWs=True):
            if token.lineNum==0: continue #Whitespace, apparently.
            tokens.append((token.lineNum,token.t))

        result = []

        #If there's a stack underflow here, it probably means your code has mismatched braces.  Check it with
        #   a real compiler.
        stack = []
        i = 0
        while True:
            if i==len(tokens): break
            line_number,token = tokens[i]
            if   token == "namespace": #[namespace] [name] [{]
                namespace = tokens[i+1][1]
                stack.append(namespace+"{")
                i += 3
            elif token == "{": #block
                stack.append(token)
                i += 1
            elif token == "}":
                stack = stack[:-1]
                i += 1
            else:
                T = [token]
                while tokens[i+1][1] == "::":
                    T.append(tokens[i+2][1])
                    i += 2
                current_namespace = []
                for entry in stack:
                    if entry != "{":
                        current_namespace.append(entry[:-1])
                #print(current_namespace)
                while len(current_namespace) > 0:
                    if T[0] == current_namespace[0]:
                        #print(tokens)
                        #input((T,"Added"))
                        result.append(line_number)
                        break
                    current_namespace = current_namespace[1:]
                i += 1

        return result
