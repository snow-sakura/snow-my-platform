package zentao.SDK.core;

import example.ExampleHttp;
import org.json.JSONException;
import org.json.JSONObject;
import zentao.Accounts;
import zentao.ZenTaoHttp;

public class LoginSDK extends ZenTaoSDKBase {
    public LoginSDK() {
        zenTaoHttp = new ZenTaoHttp(env);
        //setCookie("sessionId=XXXX");
    }

    public String getZenTaoId(String account, String password) throws JSONException {
        zenTaoHttp.isStr = true;
        bodyData.put("account", account);
        bodyData.put("password", password);
        bodyData.put("referer", "/zentaopms/www/index.php");
        return post(LOGIN_URI, getData, null, bodyData).
                getJSONObject("cookie").getString("zentaosid");
    }

    public String getZenTaoId() throws JSONException {
        return getZenTaoId(Accounts.QA_ACCOUNT, Accounts.QA_PASSWORD);
    }

    /**
     * 测试
     * @param args
     * @throws JSONException
     */
    public static void main(String[] args) throws JSONException {
        System.out.println(new LoginSDK().getZenTaoId());
    }
}
