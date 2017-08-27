# -*- coding: utf-8 -*-
import os

# You need to replace this constants
# PATH = '/Users/Yao/Downloads/TestCoordinatorLayout-master'
PATH = 'D:\\work\\TestCoordinatorLayout-master'

GRADLE_VERSION = 'gradle-3.3-all.zip'
ANDROID_GRADLE_PLUGIN = '2.3.3'
SDK_VERSION = '25'
BUILD_TOOLS_VERSION = '25.0.3'
ANDROID_SUPPORT_LIBRARY = '25.3.1'

# 针对gradle-wrapper 替换distributionUrl
file_string_list = []
target_line = -1
distributionUrl_keyword = 'distributionUrl=https\\://services.gradle.org/distributions/'
target_file = os.path.join(PATH, 'gradle', 'wrapper', 'gradle-wrapper.properties')
if os.path.isfile(target_file):
    with open(target_file, 'r') as f:
        current_line = 0;
        for line in f.readlines():
            file_string_list.append(line)
            current_line += 1
            index = line.find(distributionUrl_keyword)
            if index >= 0:
                prefix = line[0:index + distributionUrl_keyword.__len__()]
                distributionUrl_string = prefix + GRADLE_VERSION + '\n'
                target_line = current_line
    if target_line != -1:
        with open(target_file, 'w') as f:
            current_line = 0;
            for x in file_string_list:
                current_line += 1
                if target_line != current_line:
                    f.write(x)
                else:
                    f.write(distributionUrl_string)

# 针对该工程的build.gradle
file_string_list = []
target_line = -1;
androidGradlePulgin_keyword = 'classpath \'com.android.tools.build:gradle:'
target_file = os.path.join(PATH, 'build.gradle')
if os.path.isfile(target_file):
    with open(target_file, 'r') as f:
        current_line = 0;
        for line in f.readlines():
            file_string_list.append(line)
            current_line += 1
            index = line.find(androidGradlePulgin_keyword)
            if index >= 0:
                target_line = current_line
                prefix = line[0:index + androidGradlePulgin_keyword.__len__()]
                androidGradlePulgin_string = prefix + ANDROID_GRADLE_PLUGIN + '\'\n'
    if target_line != -1:
        with open(target_file, 'w') as f:
            current_line = 0;
            for x in file_string_list:
                current_line += 1
                if target_line != current_line:
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
            current_line = 0;
            for line in f.readlines():
                file_string_list.append(line)
                current_line += 1
                index = line.find(compileSdkVersion_keyword)
                if index >= 0:
                    compileSdkVersion_line = current_line
                    prefix = line[0:index + compileSdkVersion_keyword.__len__()]
                    compileSdkVersion_string = prefix + SDK_VERSION + '\n'
                    currentSdkVersion = line[index + compileSdkVersion_keyword.__len__():line.__len__()-1]
                    support_lib_split_keywrod = currentSdkVersion + "."
                index = line.find(buildToolsVersion_keyword)
                if index >= 0:
                    buildToolsVersion_line = current_line
                    prefix = line[0:index + buildToolsVersion_keyword.__len__()]
                    buildToolsVersion_string = prefix + '\"' + BUILD_TOOLS_VERSION + '\"\n'
                index = line.find(targetSdkVersion_keyword)
                if index >= 0:
                    targetSdkVersion_line = current_line
                    prefix = line[0:index + targetSdkVersion_keyword.__len__()]
                    targetSdkVersion_string = prefix + SDK_VERSION + '\n'
                if support_lib_find_keyword in line:
                    index = line.find(support_lib_split_keywrod)
                    if index >= 0:
                        prefix = line[0:index]
                        support_lib_string = prefix + ANDROID_SUPPORT_LIBRARY + '\'\n'
                        support_lib[current_line] = support_lib_string
        if compileSdkVersion_line != -1:
            with open(target_file, 'w') as f:
                current_line = 0;
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