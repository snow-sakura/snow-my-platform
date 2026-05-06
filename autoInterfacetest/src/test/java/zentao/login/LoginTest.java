package zentao.login;

import example.t1.TestCase;
import org.json.JSONException;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import util.HttpMethod;
import zentao.AssertConstant;
import zentao.SDK.core.LoginSDK;
import zentao.ZenTaoTest;

public class LoginTest extends ZenTaoTest {
    public String uri = "/zentaopms/www/index.php?m=user&f=login&referer=L3plbnRhb3Btcy93d3cvaW5kZXgucGhw";
    //  public String uri = "/zentaopms/www/index.php?m=user&f=login&referer=L3plbnRhb3Btcy93d3cvaW5kZXgucGhw%s%s";
    public HttpMethod method = HttpMethod.POST;
    private static final Logger logger = LoggerFactory.getLogger(LoginTest.class);

    /**
     * 当出现多个beforeClass时以数字字典排序
     * 比如abeforeClass,cbeforeClass则以abeforeClass先执行
     */
    @BeforeClass
    public void beforeClass() throws JSONException {
        zenTaoHttp.setHttpInfo(uri, method);
        LoginSDK loginSDK = new LoginSDK();
        String zentaoid = loginSDK.getZenTaoId();
        zenTaoHttp.headMap.put("cookie", "zentaosid=" + zentaoid);
    }


    @BeforeMethod
    public void beforeMethod() {

    }

    @AfterMethod
    public void afterMethod() {

    }

    @Test(description = "禅道登录测试", dataProvider = "testData", groups = {"smoke", "function"})
    public void testNormal(String id, String desc, String post_account, String post_password, String post_referer) throws JSONException {
        zenTaoHttp.isStr = true;
        //String[] uriParameters = {};//uri地址带参数 %s
        //setData(get_name,post_age);
        setData(post_account, post_password, post_referer);//设置数据
        //postDataMap.put("account",post_account);也可以这样传递
        //getDataMap.put("account",post_account);
        logger.info(getDataMap.toString());
        logger.info(postDataMap.toString());
//        response.setContentType("text/html;charset=utf-8"); //如果是json数据,需要设置为("text/javascript;charset=utf-8");
//        response.setcharEncoding("utf-8");
        JSONObject result = zenTaoHttp.restfulRequest(getDataMap, null, postDataMap);
        //System.out.println(result.getString("title"));
        int httpCode = result.getInt("httpcode");
        String data = result.getString("data");
        //System.out.println(data);
        System.out.println(result);
        Assert.assertEquals(httpCode, AssertConstant.HTTP_OK, "code应该是200，返回的是" + httpCode);
        Assert.assertTrue(data.contains(post_referer), "结果中不包含" + post_referer);
    }
}
