<script>
const SERVER_ADDR = '/parser/'
const WF_GRAPH_ADDR = '/wf-graph/'
const WF_SERVER_ADDR = '/wf-server/'
const GRAFANA_PORT = 3000
const GRAFANA_ADDR = 'http://' + window.location.hostname + ':' + GRAFANA_PORT + '/?orgId=1'
export default {
    SERVER_ADDR,
    WF_GRAPH_ADDR,
    WF_SERVER_ADDR,
    GRAFANA_ADDR
}
</script>
