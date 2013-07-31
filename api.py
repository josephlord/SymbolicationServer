from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource
from subprocess import Popen, check_output
from json import dumps

app = Flask(__name__)
api = Api(app)

symbolicateApp = "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/PrivateFrameworks/DTDeviceKit.framework/Versions/A/Resources/symbolicatecrash"
# export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer


class Symbolicate(Resource):
    def post(self):
#        print request.form
        crashlog = request.form['crashlog']
        print crashlog
        symbolicator = Popen([symbolicateApp, '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        (symbolicated, meta) = symbolicator.communicate(crashlog)
        print meta
        print symbolicated
        return {'symbolicatedCrashlog': symbolicated, 'symbolicatorMetaOutput': meta}

api.add_resource(Symbolicate, '/symbolicate')


def jsonify_crash_for_testing():
    inputFileName = "Fast_Lists-2013-07-19-11-46.crash"
    origFileText = check_output(["cat", inputFileName])
    origAsDict = {'crashlog': origFileText}
    jsontext = dumps(origAsDict)
    print jsontext


if __name__ == '__main__':
   # jsonify_crash_for_testing()
    app.run(debug=True)
