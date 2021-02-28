if __name__ == "__main__":
    import argparse
    import json
    import os
    import zipfile
    from base.docxhandler import DocxHandler as dh
    from base.exceptions import *
    from base.fontmapper import FontMapper as fm
    from base.txthandler import TxtHandler as th
    about = """ 
    Created by : Sabin Acharya (@trippygeese on github)
    License    :       
    Version    : v0.2A
    Email      : sabin2059@protonmail.com
    """
    modes = ['string', 'plain', 'docx']
    parser = argparse.ArgumentParser(description=about, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version="0.1a")
    parser.add_argument('-m', '--mode', dest='mode', help='Conversion mode ', choices=modes, required=True)
    parser.add_argument('-f', '--font', dest='font', help='Font used in input file. ("auto" can be used for docx mode)', default='preeti', required=True)
    parser.add_argument('-of', '--output-font', dest='outputfont', help='Font to which output will be mapped to. (If unspecified opuput font will be set to unicode)', default='unicode', choices=["Preeti", "unicode"], required=False)
    parser.add_argument('-dc', '--docx-components', dest='docxcomponents', help='Component of docx which will be processed. (Comma seperated) Available: "body_paragraph,table,shape" (If not specified all components will be processed)', default='body_paragraph,table,shape', required=False)
    parser.add_argument('-kf', '--known-unicode-fonts', dest='knownunicodefonts', help='Fonts to add to known supported unicode fonts while converting to preeti (If Unspecified "Kalimati,Mangal,Noto Sans Devanagari" will be set)', default='', required=False)
    parser.add_argument('-i', '--input', dest='input', help='Input string or filepath', required=True)
    parser.add_argument('-o', '--output', dest='output', help='Output file path. Not required for string mode')
    parser.add_argument('-mf', '--map-file', dest='mapfile', help='Mapping defination file')
    args = parser.parse_args()
    font = args.font
    op_mode = args.mode
    def splitnclean(string):
        lis = split(string)
        for index, item in enumerate(lis):
            lis[index] = item.strip()
        return lis

    rule_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "map.json")
    if args.mapfile is not None:
        rule_file = args.mapfile
    if op_mode == "string":
        try:
            converter = fm(rule_file)
            if args.outputfont == 'unicode':
                print(converter.map_to_unicode(args.input, from_font=args.font))
            elif args.outputfont == 'Preeti':
                print(converter.map_to_preeti(args.input, from_font=args.font))
            else:
                raise UnsupportedMapToException
        except NoMapForOriginException:
            print("The mapping for selected origin font does not exist")
        except FileNotFoundError:
            print("Mapping defination file cannot be opened or does not exist.")
        except json.decoder.JSONDecodeError:
            print("Invalid mapping defination file")
        except UnsupportedMapToException:
            print("Cannot map to specified output font")
        except Exception as e:
            print("Unexpected error... Exiting !  "+str(e))
    elif op_mode == "plain" or op_mode == "docx":
        converter = None
        try:
            if op_mode == "plain":
                converter = th(rule_file)
            elif op_mode == "docx":
                converter = dh(rule_file)
            converter.map_fonts(orginal_file_path=args.input, output_file_path=args.output, from_font=args.font, to_font=args.outputfont, components=splitnclean(args.docxcomponents), known_unicode_fonts=splitnclean(args.knownunicodefonts))
            print("Converted !")
        except NoMapForOriginException:
            print("The mapping for selected origin font does not exist")
        except FileNotFoundError:
            print("Mapping defination file cannot be opened or does not exist.")
        except json.decoder.JSONDecodeError:
            print("Invalid mapping defination file")
        except UnsupportedMapToException:
            print("Cannot map to given output font !")
        except TxtAutoModeException:
            print("Font autodetection does not work on txt files :(")
        except zipfile.BadZipFile:
            print("Improper docx file")
        except Exception as e:
            print("Unexpected error... Exiting !  "+str(e))
    else:
        print("Unsupported operation mode")
else:
    from .base.fontmapper import *
    from .base.docxhandler import *
    from .base.txthandler import *
    from .base.exceptions import *
