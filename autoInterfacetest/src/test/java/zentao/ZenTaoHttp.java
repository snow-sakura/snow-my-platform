package zentao;

import example.ExampleHttp;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import util.BaseHttp;
import util.HttpMethod;
import util.Tool;

import java.util.Map;

public class ZenTaoHttp extends BaseHttp {
    private static final Logger logger = LoggerFactory.getLogger(ZenTaoHttp.class);
    public String example_url = "";

    public ZenTaoHttp() {
    }

    public ZenTaoHttp(String env) {
        BaseHttp.env = env;
        this.headMap.put("Content-Type", "application/json;charset=utf-8");
        loadCommConf();
    }

    public void loadCommConf() {
        ps = Tool.getProperties("conf/zentao.properties");
        this.example_url = ps.getProperty(env + "_zentao_url");
    }


    public void setMethod(HttpMethod method) {
        this.method = method;
    }

    public void setURI(String uri) {
        this.url = example_url + uri;
    }

    public void setData(Map<String, Object> data) {
        if (data != null) {
            this.data = data;
        }
    }

    public void setHttpInfo(String uri, HttpMethod method) {
        setURI(uri);
        setMethod(method);
    }
}
