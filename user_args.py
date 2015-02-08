"""
To handle input args & subsequent modifications
"""


import argparse
import os.path
import helper_methods as helpr
import requisite_checker as checkr


def get_args():
    """Define all command-line options. Returns ArgumentParser object."""

    parser = argparse.ArgumentParser(
        description="Convert MC event into particle evolution diagram.\n"
                    "Uses dot/GraphViz/dot2tex/pdflatex to make a PDF.",
        # formatter_class=argparse.ArgumentDefaultsHelpFormatter
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Input options
    parser.add_argument("input",
                        help="Input file",
                        nargs="?",
                        default="qcdScatterSmall.txt")
    parser.add_argument("--inputFormat",
                        help="Input format. If unspecified, will try and "
                             "make an educated guess, but could fail!",
                        choices=["HEPMC", "PYTHIA"])
    parser.add_argument("--eventNumber",
                        help="Select event number to plot (for input formats "
                             "HEPMC)",
                        type=int, default=0)

    # Output file options
    # parser.add_argument("-oGV", "--outputGV",
    #                     help="output GraphViz filename "
    #                          "(if unspecified, defaults to INPUT.gv)")
    parser.add_argument("-O", "--outputPDF",
                        help="Output PDF filename "
                             "(if unspecified, defaults to INPUT.pdf)")
    parser.add_argument("--openPDF",
                        help="Automatically open PDF once plotted",
                        action="store_true")

    # Render options
    parser.add_argument("-p", "--particleMode",
                        choices=["NODE", "EDGE"],
                        help="Particle representation (see README)")
    parser.add_argument("--noPDF",
                        help="Don't convert to PDF",
                        action="store_true")

    # Check to see if certain render modes are available.
    # If not, don't give them to the user as options
    render_opts = {"DOT": "Fast, but basic formatting",
                   "LATEX": "Slower, but nicer formatting"}

    latex_check = checkr.RequisiteChecker(modules=["pydot", "pyparsing"],
                                          programs=["dot2tex"])
    if not latex_check.all_exist:
        del render_opts["LATEX"]

    dot_check = checkr.RequisiteChecker(programs=["dot"])
    if not dot_check.all_exist:
        del render_opts["DOT"]

    if len(render_opts.keys()) == 0:
        raise EnvironmentError("You are mising programs. Cannot render.")

    help_str = ""
    for k, v in render_opts.items():
        help_str += k + ": " + v + "\n"

    parser.add_argument("-r", "--render",
                        help="Render method:\n%s" % help_str,
                        choices=render_opts,
                        default="DOT")

    # Testing options
    parser.add_argument("--straightEdges",
                        help="Use straight edges instead of curvy",
                        action="store_true")
    parser.add_argument("--showVertexBarcode",  # think of a better opt name!
                        help="Show vertex barcodes, useful for figuring out "
                             "which are the hard interaction(s). Only useful "
                             "when in EDGE mode.",
                        action="store_true")
    parser.add_argument("--hardVertices",
                        help='List of vertex barcode(s) that contain the '
                             'hard interaction, e.g. --hardVertices V2, V3 '
                             '(LATEX render only)',
                        default=None, nargs='*', type=str)
    parser.add_argument("--noTimeArrows",
                        help='Turn off the "Time" arrows (LATEX render only)',
                        action="store_true")
    parser.add_argument("--scale",
                        help="Factor to scale PDF by (LATEX render only)",
                        default=0.7, type=float)
    parser.add_argument("-v", "--verbose",
                        help="Print debug statements to screen",
                        action="store_true")

    args = parser.parse_args()

    # Post process user args
    set_default_output(args)
    set_default_format(args)
    set_default_mode(args)

    if args.verbose:
        from pprint import pprint; pprint(args)

    return args


def set_default_output(args):
    """Set default output filenames and stems/dirs"""
    args.input = helpr.cleanup_filepath(args.input)  # sanitise input
    args.in_name = os.path.basename(args.input)  # just filename and extension
    args.stem_name, args.extension = os.path.splitext(args.in_name)
    args.in_dir = helpr.get_full_path(args.input)

    # Set default PDF filename if not already done
    if not args.outputPDF:
        args.outputPDF = os.path.join(args.in_dir, args.stem_name+".pdf")

    # Set default graphviz filename from PDF name
    args.outputGV = args.outputPDF.replace(".pdf", ".gv")


def set_default_format(args):
    """Set default input format if the user hasn't."""
    if not args.inputFormat:
        if args.extension == ".hepmc":
            args.inputFormat = "HEPMC"
        elif args.extension in [".txt", ".out"]:
            args.inputFormat = "PYTHIA"
        print "You didn't set an input format. Assuming", args.inputFormat


def set_default_mode(args):
    """Set default particle mode if the user hasn't."""
    if not args.particleMode:
        if args.inputFormat == "HEPMC":
            args.particleMode = "EDGE"
        else:
            args.particleMode = "NODE"
    print "You didn't set a particle mode. Using", args.particleMode