function scp_cmd()
{
    local ip=$1
    local usr=$2
    local passwd=$3
    srcfile=$4
    desfile=$5
    opt=$6
    case $opt in
        file)
                expect -c "
            spawn scp -r $srcfile $usr@$ip:$desfile
                set timeout  -1
                expect {
                        \"*no)?\"  {
                                send \"yes\r\"
                                exp_continue
                        }
                        \"*assword:*\"  {
                                send \"$passwd\r\"
                                exp_continue
                        }
                }
                "
        ;;
        dir)
            expect -c "
                        spawn scp -r $srcfile $usr@$ip:$desfile
                        set timeout  -1
                        expect {
                                \"*no)?\"  {
                                        send \"yes\r\"
                                        exp_continue
                                }
                                \"*assword:*\"  {
                                        send \"$passwd\r\"
                                        exp_continue
                                }
                        }
                        "
        ;;
        *)
            echo "err"
        ;;
    esac
}

function remote_scp_cmd()
{
    local ip=$1
    local usr=$2
    local passwd=$3
    srcfile=$4
    desfile=$5
    opt=$6
    case $opt in
        file)
                expect -c "
                spawn scp -r $usr@$ip:$srcfile $desfile
                set timeout  -1
                expect {
                        \"*no)?\"  {
                                send \"yes\r\"
                                exp_continue
                        }
                        \"*assword:*\"  {
                                send \"$passwd\r\"
                                exp_continue
                        }
                }
                "
        ;;
        dir)
            expect -c "
                        spawn scp -r $usr@$ip:$srcfile $desfile
                        set timeout  -1
                        expect {
                                \"*no)?\"  {
                                        send \"yes\r\"
                                        exp_continue
                                }
                                \"*assword:*\"  {
                                        send \"$passwd\r\"
                                        exp_continue
                                }
                        }
                        "
        ;;
        *)
            echo "err"
        ;;
    esac
}
