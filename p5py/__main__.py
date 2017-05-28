import sys
from . import _p5

# we should be parsing sys args here and expose a series of commands
# similar to processing-java.
#
# relevant output from `processing-java --help`:
#
#     --help               Show this help text. Congratulations.
#    
#     --sketch=<name>      Specify the sketch folder (required)
#     
#     --output=<name>      Specify the output folder (optional and
#                          cannot be the same as the sketch folder.)
#                          
#     --force              The sketch will not build if the output
#                          folder already exists, because the contents
#                          will be replaced. This option erases the
#                          folder first. Use with extreme caution!
#                          
#     --build              Preprocess and compile a sketch into .class files.
#     
#     --run                Preprocess, compile, and run a sketch.
#     
#     --present            Preprocess, compile, and run a sketch in presentation mode.
#    
#     --export             Export an application.
#     
#     --no-java            Do not embed Java. Use at your own risk!
#     
#     --platform           Specify the platform (export to application only).
#                          Should be one of 'windows', 'macosx', or 'linux'.
#
                                                                                    
