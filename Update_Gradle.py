# -*- coding: utf-8 -*-
import os, re

# You need to replace this constants
# PATH = '/Users/Yao/Downloads/TestCoordinatorLayout-master'
PATH = 'D:\\work_py\\TestCoordinatorLayout-master'

GRADLE_VERSION = 'gradle-3.3-all.zip'
ANDROID_GRADLE_PLUGIN = '2.3.3'
SDK_VERSION = '25'
BUILD_TOOLS_VERSION = '25.0.3'
ANDROID_SUPPORT_LIBRARY = '25.3.1'

# 针对gradle-wrapper 替换distributionUrl
file_string_list = []
distributionUrl_keyword = 'distributionUrl=https\\://services.gradle.org/distributions/'
target_file = os.path.join(PATH, 'gradle', 'wrapper', 'gradle-wrapper.properties')
if os.path.isfile(target_file):
    with open(target_file, 'r') as f:
        current_line = 0
        for line in f.readlines():
            file_string_list.append(line)
            current_line += 1
            index = line.find(distributionUrl_keyword)
            if index >= 0:
                distributionUrl_line = current_line
                distributionUrl_string = re.sub('gradle-[\w\.-]+-all\.zip', GRADLE_VERSION, line)
    if distributionUrl_line != -1:
        with open(target_file, 'w') as f:
            current_line = 0
            for x in file_string_list:
                current_line += 1
                if distributionUrl_line != current_line:
                    f.write(x)
                else:
                    f.write(distributionUrl_string)

# 针对该工程的build.gradle
file_string_list = []
androidGradlePulgin_keyword = 'classpath \'com.android.tools.build:gradle:'
target_file = os.path.join(PATH, 'build.gradle')
if os.path.isfile(target_file):
    with open(target_file, 'r') as f:
        current_line = 0
        for line in f.readlines():
            file_string_list.append(line)
            current_line += 1
            index = line.find(androidGradlePulgin_keyword)
            if index >= 0:
                androidGradlePulgin_line = current_line
                androidGradlePulgin_string = re.sub('(?<=:)[\d\.]+(?=\')', ANDROID_GRADLE_PLUGIN, line)
    if androidGradlePulgin_line != -1:
        with open(target_file, 'w') as f:
            current_line = 0
            for x in file_string_list:
                current_line += 1
                if androidGradlePulgin_line != current_line:
                    f.write(x)
                else:
                    f.write(androidGradlePulgin_string)

# 针对每个module的build.gradle
compileSdkVersion_line = -1
compileSdkVersion_keyword = 'compileSdkVersion '
buildToolsVersion_line = -1
buildToolsVersion_keyword = 'buildToolsVersion '
targetSdkVersion_line = -1
targetSdkVersion_keyword = 'targetSdkVersion '
support_lib = {} #key为行数,value为前缀
support_lib_find_keyword = 'com.android.support:'

dir_list = [x for x in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, x)) and not x.startswith('.') and not x == 'gradle']
# print(dir_list)
for target_file in dir_list:
    file_string_list = []
    target_file = os.path.join(PATH, target_file, 'build.gradle')
    if os.path.isfile(target_file):
        with open(target_file, 'r') as f:
            current_line = 0
            for line in f.readlines():
                file_string_list.append(line)
                current_line += 1
                index = line.find(compileSdkVersion_keyword)
                if index >= 0:
                    compileSdkVersion_line = current_line
                    sdk_version_regex = '(?<=compileSdkVersion\s)\d+'
                    compileSdkVersion_string = re.sub(sdk_version_regex, SDK_VERSION, line)
                    currentSdkVersion = re.search(sdk_version_regex, line).group()
                    support_lib_split_keywrod = currentSdkVersion + "." #com.android.support的各个依赖库  需要那sdk版本号这个数字来匹配关键字
                index = line.find(buildToolsVersion_keyword)
                if index >= 0:
                    buildToolsVersion_line = current_line
                    buildToolsVersion_string = re.sub('(?<=buildToolsVersion\s\")[\d\.]+(?=\")', BUILD_TOOLS_VERSION, line)
                index = line.find(targetSdkVersion_keyword)
                if index >= 0:
                    targetSdkVersion_line = current_line
                    targetSdkVersion_string = re.sub('(?<=targetSdkVersion\s)\d+', SDK_VERSION, line)
                if support_lib_find_keyword in line:
                    support_lib_string = re.sub('(?<=:)' + currentSdkVersion + '\.[\d\.]+(?=\')', ANDROID_SUPPORT_LIBRARY, line)
                    support_lib[current_line] = support_lib_string
        if compileSdkVersion_line != -1:
            with open(target_file, 'w') as f:
                current_line = 0
                for x in file_string_list:
                    current_line += 1
                    if current_line == compileSdkVersion_line:
                        f.write(compileSdkVersion_string)
                    elif current_line == buildToolsVersion_line:
                        f.write(buildToolsVersion_string)
                    elif current_line == targetSdkVersion_line:
                        f.write(targetSdkVersion_string)
                    elif current_line in support_lib:
                        f.write(support_lib[current_line])
                    else:
                        f.write(x)