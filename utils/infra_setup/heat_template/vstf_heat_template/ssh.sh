function run_cmd()
{
    local ip=$1
    local usr=$2
    local passwd=$3
    local cmd=$4
    expect -c "
        spawn ssh $usr@$ip
        set timeout -1
        expect {
                \"*no)?\"  {
                        send \"yes\r\"
                        exp_continue
                }
                \"*assword:*\"  {
                        send \"$passwd\r\"
            exp_continue
                }
        \"*#\"  {
            send \"$cmd\r\"
            exec sleep 1
            send \"exit\r\"
            expect eof
        }
            }
    "
}

