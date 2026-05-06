package zentao.project;

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
import zentao.SDK.core.LoginSDK;
import zentao.ZenTaoTest;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Random;


public class CreateProjectTest extends ZenTaoTest {

    public String uri = "/zentaopms/www/index.php?m=project&f=create";
    public HttpMethod method = HttpMethod.POST;
    private static final Logger logger = LoggerFactory.getLogger(CreateProjectTest.class);
    private Random ran = new Random();
    /**
     * 当出现多个beforeClass时以数字字典排序
     * 比如abeforeClass,cbeforeClass则以abeforeClass先执行
     */
    @BeforeClass
    public void beforeClass() throws JSONException {
        zenTaoHttp.setHttpInfo(uri, method);
        //创建login sdk 对象
        LoginSDK loginSDK = new LoginSDK();
        //获取sessionId
        String zentaoid = loginSDK.getZenTaoId();
        //把sessionId加入到cookie中
        zenTaoHttp.headMap.put("cookie", "zentaosid=" + zentaoid);
    }


    @BeforeMethod
    public void beforeMethod() {

    }

    @AfterMethod
    public void afterMethod() {

    }

    @Test(description = "禅道创建项目测试",dataProvider = "testData",groups = {"smoke","function"})
    public void testNormal(String id,String desc,String name,String code,String begin,
                           String end,int days,String team,String type,int products0,
                           String p_desc,String acl,String uid) throws JSONException, ParseException {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        //String date = dateFormat.format(new Date());
        String beginDates = dateFormat.format(new Date(begin));
        String endDates = dateFormat.format(new Date(end));
        if(name!=null&&name.equals("uuid")){
            name = System.currentTimeMillis()+ran.nextInt()+"";
        }
        if(code!=null&&code.equals("random")){
            code = name;
        }
        if (p_desc!=null&&p_desc.equals("time")){
            p_desc = System.currentTimeMillis()+"";
        }

        postDataMap.put("name",name);
        postDataMap.put("code",code);
        postDataMap.put("begin",beginDates);
        postDataMap.put("end",endDates);
        postDataMap.put("days",days);
        postDataMap.put("team",team);
        postDataMap.put("type",type);
        postDataMap.put("products[0]",products0);
        postDataMap.put("desc",p_desc);
        postDataMap.put("acl",acl);
        postDataMap.put("uid",uid);
        zenTaoHttp.isStr=true;
        JSONObject json = zenTaoHttp.restfulRequest(getDataMap,null,postDataMap);
        //todo
    }

    @Test(description = "禅道创建项目测试-反向",dataProvider = "testData",groups = {"fail","function"})
    public void testFail(String id,String desc,String name,String code,String begin,
                           String end,int days,String team,String type,int products0,
                           String p_desc,String acl,String uid,String message) throws JSONException {
        postDataMap.put("name",name);
        postDataMap.put("code",code);
        postDataMap.put("begin",begin);
        postDataMap.put("end",end);
        postDataMap.put("days",days);
        postDataMap.put("team",team);
        postDataMap.put("type",type);
        postDataMap.put("products[0]",products0);
        postDataMap.put("desc",p_desc);
        postDataMap.put("acl",acl);
        postDataMap.put("uid",uid);
        zenTaoHttp.isStr=true;
        JSONObject json = zenTaoHttp.restfulRequest(getDataMap,null,postDataMap);
        String result = json.getString("data");
        Assert.assertTrue(result.contains(message),"错误提示不正确，期望的message："+ message);
        //Assert.assertTrue(result.contains(message+"123"),"错误提示不正确，期望的message："+ message);
    }
}
