function addClass(element, className) {
    var classString = element.getAttribute("class");
    if(classString == null) {
        element.setAttribute("class", " " + className);
    } else {
        if(isContainClass(element, className) == -1) {
            classString += " " + className;
            element.setAttribute("class", classString);
        }
    }
}

function removeClass(element, className) {
    var start = isContainClass(element, className);
    if(start != -1) {
        var classString = element.getAttribute("class");
        classString = classString.replace(className, " ");
        element.setAttribute("class", classString);
    }
}

function isContainClass(element, className) {
    var classString = element.getAttribute("class");
    if(classString == null) {
        return -1;
    } else {
        if(classString.indexOf(className) == -1) {
            return -1;
        } else {
            if(classString[0] == ' ') {
                classString = classString.substr(1);
            }
            if(classString[classString.length - 1] == ' ') {
                classString = classString.substr(0, classString.length - 1);
            }

            if(classString == className) {
                return 0;
            }

            // classString contains multi-classes.
            var start = classString.indexOf(className);
            var end = start + className.length - 1;
            if(start == 0 && classString[end + 1] == ' ') { 
                return start;
            } 
            else if(end = (classString.length - 1) && classString[start - 1] == ' ') {
                return start;
            }
            else if(classString[start - 1] == ' ' && classString[end + 1] == ' ') {
                return start;
            } 
            else {
                return -1;
            }
        }
    }
}



function timestampToTime(timestamp) {
    var date = new Date(timestamp);
    Y = date.getFullYear() + '-';
    M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
    D = date.getDate() + ' ';
    h = date.getHours() + ':';
    m = date.getMinutes() + ':';
    s = date.getSeconds();
    return Y+M+D+h+m+s;
}

export {
    addClass,
    removeClass,
    isContainClass,
    timestampToTime
}