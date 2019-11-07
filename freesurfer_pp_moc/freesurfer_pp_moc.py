#!/usr/bin/env python                                            
#                                                             _
# freesurfer_pp_moc ds app
#
# (c) 2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import  os
from    os          import listdir, sep
from    os.path     import abspath, basename, isdir
import  shutil
import  pudb
import  sys
import  time
import  glob

# import the Chris app superclass
from chrisapp.base import ChrisApp

Gstr_title = """
  __                               __                                              
 / _|                             / _|                                             
| |_ _ __ ___  ___ ___ _   _ _ __| |_ ___ _ __   _ __  _ __   _ __ ___   ___   ___ 
|  _| '__/ _ \/ _ | __| | | | '__|  _/ _ \ '__| | '_ \| '_ \ | '_ ` _ \ / _ \ / __|
| | | | |  __/  __|__ \ |_| | |  | ||  __/ |    | |_) | |_) || | | | | | (_) | (__ 
|_| |_|  \___|\___|___/\__,_|_|  |_| \___|_|    | .__/| .__/ |_| |_| |_|\___/ \___|
                                          ______| |   | |______                    
                                         |______|_|   |_|______|                   

"""

Gstr_synopsis = """

    NAME

        freesurfer_pp_moc.py

    SYNOPSIS

        python freesurfer_pp_moc.py                                         \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--copySpec <copySpec>]                                     \\
            [--ageSpec <ageSpec>]
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * To copy some directory in open storage to an output directory:

            mkdir out
            python pacscopy.py      --dir <someDirInOpenStorage>        \\
                                    out

    DESCRIPTION

        `pacscopy.py` simply copies a directory specified with the 
        `--dir <dir>` flag-value pair to the output directory.

    ARGS

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number. 
        
        [--man]
        If specified, print (this) man page.

        [--meta]
        If specified, print plugin meta data.

        [-T <targetTreeHead>] | [--treePrint <targetTreeHead>]
        Print a simple directory tree rooted on <targetTreeHead>. Typically
        used to print the internal database with a 
        
                    -T ../preprocessed

        [-a <ageSpec>] | [--ageSpec <ageSpec>]
        A string in <YY>-<MM>-<DD> format that denotes an *exact* target to
        retrieve. Consult '-T ../preprocessed' to see full range of specs.

        [-c <copySpec>] | [--copySpec <copySpec>]
        A comma separated string denoting the preprocessed subdirs to copy. 
        Note that a substring glob is performed, thus a spec of 'tra' will
        target 'aparc.a2009s+aseg-LUT-tra'.

        [-P <processDelay>] | [--processDelay <processDelay>]
        A delay timer to simulate remote processing. The script will pause for
        <processDelay> seconds.
"""

class Freesurfer_pp_moc(ChrisApp):
    """
    A "dummy" app containing the output of some prior FreeSurfer runs, 
    organized in
    
            <YR>-yr/<MO>-mo/<DA>-da
            
    directory structure within the container. This app simply copies one 
    of these pre-processed output trees into the output folder of the plugin.
    
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'FreeSurfer Pre-Populated'
    CATEGORY                = 'FreeSurfer'
    TYPE                    = 'ds'
    DESCRIPTION             = 'A "dummy" app that contains some prior FreeSurfer output and simply copies this to the output directory.'
    DOCUMENTATION           = 'https://github.com/FNNDSC/pl-freesurfer_pp_moc'
    VERSION                 = '2.2.0'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Fill out this with key-value output descriptive info (such as an output file path
    # relative to the output dir) that you want to save to the output meta file when
    # called with the --saveoutputmeta flag
    OUTPUT_META_DICT        = {}
 
    str_tree                = ''

    def show_man_page(self):
        """
        Print some quick help.
        """
        print(Gstr_synopsis)

    @staticmethod
    def dirTree_probe(dir, padding, print_files=False):
        """
        Simple method that returns a string of a dir tree layout. 

        Relies on global variable, <str_tree>!!!
        """
        Freesurfer_pp_moc.str_tree += padding[:-1] + '+-' + basename(abspath(dir)) + '/' + '\n'
        padding = padding + ' '
        files = []
        if print_files:
            files = listdir(dir)
        else:
            files = [x for x in listdir(dir) if isdir(dir + sep + x)]
        count = 0
        for file in files:
            count += 1
            Freesurfer_pp_moc.str_tree += padding + '|' + '\n'
            path = dir + sep + file
            if isdir(path):
                if count == len(files):
                    Freesurfer_pp_moc.dirTree_probe(path, padding + ' ', print_files)
                else:
                    Freesurfer_pp_moc.dirTree_probe(path, padding + '|', print_files)
            else:
                Freesurfer_pp_moc.str_tree += padding + '+-' + file + '\n'
        return Freesurfer_pp_moc.str_tree
    
    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """
        self.add_argument("-T", "--treePrint",
                            help        = "Simple dirtree print. Specify head of target tree",
                            type        = str,
                            dest        = 'treePrint',
                            optional    = True,
                            default     = "")
        self.add_argument("-a", "--ageSpec",
                            help        = "A string in <YY>-<MM>-<DD> format that denotes an *exact* target to retrieve",
                            type        = str,
                            dest        = 'ageSpec',
                            optional    = True,
                            default     = "")
        self.add_argument("-c", "--copySpec",
                            help        = "A comma separated string denoting the subdirs to copy",
                            type        = str,
                            dest        = 'copySpec',
                            optional    = True,
                            default     = "stats")
        self.add_argument("-P", "--processDelay",
                            help        = "delay timer to simulate remote processing",
                            type        = str,
                            dest        = 'processDelay',
                            optional    = True,
                            default     = "0")
        self.add_argument("--jsonReturn",
                            help        = "output final return in json",
                            type        = bool,
                            dest        = 'jsonReturn',
                            action      = 'store_true',
                            optional    = True,
                            default     = False)

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """

        if len(options.treePrint):
            str_tree = ''
            str_tree = Freesurfer_pp_moc.dirTree_probe(options.treePrint, '')
            print(str_tree)
            sys.exit(0)

        print(Gstr_title)
        print('Version: %s' % Freesurfer_pp_moc.VERSION)

        if len(options.processDelay):
            print('Simulating a process delay of %s seconds...' % options.processDelay)
            time.sleep(int(options.processDelay))

        str_ageDirDefault   = '10-yr/06-mo/01-da'
        if len(options.ageSpec):
            l_ageSpec   = options.ageSpec.split('-')
            str_ageDir  = '%s-yr/%s-mo/%s-da' % (l_ageSpec[0], l_ageSpec[1], l_ageSpec[2])
        else:
            str_ageDir  = str_ageDirDefault

        str_treeAgeSpec = '../preprocessed/%s' % str_ageDir
        if not os.path.isdir(str_treeAgeSpec):
            print('It seems the ageSpec dir does not seem valid. Reverting to default.')
            str_treeAgeSpec = '../preprocessed/%s' % str_ageDirDefault            

        # pudb.set_trace()
        lstr_targetDir  = options.copySpec.split(',')
        for str_targetDir in lstr_targetDir:
            lstr_targetDirFull   = glob.glob("%s/*%s*" % (options.outputdir, str_targetDir))
            if len(lstr_targetDirFull): 
                print('Deleting any pre-existing data in output dir: %s...' % lstr_targetDirFull[0])
                shutil.rmtree('%s' % (lstr_targetDirFull[0]), ignore_errors = True)
            lstr_sourceDir   = glob.glob('%s/*%s*' % (str_treeAgeSpec, str_targetDir))
            if len(lstr_sourceDir):
                str_targetDirFull   = '%s/%s' % \
                    (options.outputdir, os.path.basename(lstr_sourceDir[0]))
                if os.path.isdir(lstr_sourceDir[0]):
                    print('Copying tree from %s to %s...' % \
                        (lstr_sourceDir[0], str_targetDirFull))
                    shutil.copytree(lstr_sourceDir[0], str_targetDirFull)

# ENTRYPOINT
if __name__ == "__main__":
    app = Freesurfer_pp_moc()
    app.launch()
