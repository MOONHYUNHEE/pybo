//넘어 온 값이 빈 값인지 체크
// [],{}도 빈값으로 처리

// null 값을 체크하는 역할
let isEmpty=function(value){
    if(""==value || null ==value || undefined == value || ( value != null && typeof value == "object" && !Object.keys(value).length)){
        return true;
    }else{
        return false;
    }
};