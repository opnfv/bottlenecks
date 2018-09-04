import toastr from '../../assets/js/toastr.min.js'
export default function(type, title, info, detail="") {
    if(typeof type == "number") {
        if(200 <= type && type < 300) {
            type = "success";
        } else if (300 <= type && type < 500) {
            type = "warning";
        } else if (500 <= type) {
            type = "error";
        } else {
            type = "info";
        }
    }
    if(detail != "") {
        detail = "* <strong>detail:</strong>  " + detail;
    }
    var content = "<br>* " + info + "<br><br>" + detail;
    if(type == "success"){
        toastr.success(content, title);
    }
    else if(type == "info") {
        toastr.info(content, title);
    }
    else if(type == "error"){
        toastr.error(content, title);
    }
    else {
        toastr.warning(content, title);
    }
}
