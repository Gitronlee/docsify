# vue项目起步及知识点小记

此处记录前端小白的起步之路。

## 一、安装nodejs

1. 执行以下命令安装nodejs及npm
   
   ```bash
   sudo apt-get install nodejs
   sudo apt install nodejs-legacy
   sudo apt install npm
   ```
2. 但是遇到了问题：
   ```
   下列软件包有未满足的依赖关系：
   E：无法修正错误，因为您要求某些软件包保持现状，就是它们破坏了软件包间的依赖关系。 npm ：依赖：node-gyp（>- 9.10.9）但是它将不会被安装 -
   ```
   解决方法为：<font color=red>软件和更新</font>勾选 <font color=red>可从互联网下载 Canonical 支持的免费和开源软件(main)</font> 和 <font color=red>社区维护的免费和开源软件(universe) </font>
   执行 ```sudo apt-get update```
3. 更换淘宝的镜像
   ```sudo npm config set registry https://registry.npm.taobao.org```
4. 安装更新版本的工具N，执行：
   ```sudo npm install n -g```
5. 更新新node版本，执行：
   ```sudo n stable```
6. 安装 cnpm ```sudo npm install cnpm -g```
7. 安装SASS加速器
```sudo cnpm install sass-loader node-sass --save-dev```
## 二、安装vue-cli
1. 使用cnpm安装vue-cli,其中  
对于vue-cli2 ： ```sudo cnpm install vue-cli -g```
对于vue-cli3：```npm install -g @vue/cli```(我用的vue-cli3)
2. 启动测试
对于vue-cli2 ：```npm run dev```
对于vue-cli3：```npm run serve```
## 三、 一键构建目录结构

```vue create project-name```此处我选择的是 vue2.x
一路回车固然简单，但是最好将各种lint test项先no之，避免起步的各种报错~
## 四、知识点小记
1. 阻止显示生产模式的消息
生产模式：`npm run build` 打包之后给后端放在服务端上用的。```Vue.config.productionTip = false```的意思是阻止显示生产模式的消息。
2. new Vue 和 store
一个 Vue 应用由一个通过 new Vue 创建的根 Vue 实例，以及可选的嵌套的、可复用的组件树组成。当一个 Vue 实例被创建时，它将 data 对象中的所有的属性加入到 Vue 的响应式系统中。每一个 Vuex 应用的核心就是 store（仓库）。“store”基本上就是一个容器，它包含着你的应用中大部分的<font color=green>状态 (state)</font> 。
    ```js
    new Vue({
        router,
        store,
        render: h => h(App)
    }).$mount('#app')
    ```
    `render: h => h(App)` 是下面内容的缩写：
    ```js
    render: function (createElement) {
        return createElement(App);
    }
    ```
3. 在项目运行中，main.js作为项目的入口文件，运行中，找到其实例需要挂载的位置，即index.html中，刚开始，index.html的挂载点处的内容会被显示，但是随后就被实例中的组件中的模板中的内容所取代，所以我们会看到有那么一瞬间会显示出index.html中正文的内容。在main.js中```Vue.use(Antd);Vue.use(VueContextMenu)```添加全局的功能插件。

4. export default 和 export ：
- export与export default均可用于导出常量、函数、文件、模块等
- 可以在其它文件或模块中通过import+(常量 | 函数 | 文件 | 模块)名的方式，将其导入，以便能够对其进行使用
- 在一个文件或模块中，export、import可以有多个，export default仅有一个
- 通过export方式导出，在导入时要加{ }，export default则不需要
5. 使用并安装必要的组件
ant-design-vue、js-cookie
    ```js
    import Antd from 'ant-design-vue';
    import 'ant-design-vue/dist/antd.css';
    import Cookies from 'js-cookie'
    import VueContextMenu from 'vue-contextmenu'
    ```
    安装命令分别为
    ```bash
    cnpm install ant-design-vue --save
    cnpm install js-cookie --save
    cnpm install --save vue-contextmenu
    ```
1. 使用VUEX
    ```js
    //mapState(['nickname'])映射为：
    nickname(){
    return this.$store.state.nickname
    }
    //mapGetters(['realname'])映射为：
    realname(){
    return this.$store.getters.realname
    }
    //mapMutations(['addAge'])映射为：
    addAge(payLoad){
    this.$store.commit('addAge',payLoad)
    }
    //mapActions(['getUserInfo']) 映射为：
    getUserInfo(){
    return this.$store.dispatch(‘getUserInfo’)
    }
    ```
1. ```this.$store.dispatch() ```与 ```this.$store.commit()```方法的区别总的来说他们只是存取方式的不同,两个方法都是传值给vuex的mutation改变state.
    - this.$store.dispatch() ：含有异步操作，例如向后台提交数据，写法：this.$store.dispatch(‘action方法名’,值)
    存储 this.$store.dispatch('getlists',name)  
    取值 this.$store.getters.getlists
    - this.$store.commit()：同步操作，，写法：this.$store.commit(‘mutations方法名’,值)
    存储 this.$store.commit('changeValue',name)  
    取值 this.$store.state.changeValue
1. 通俗的讲，ref特性就是为元素或子组件赋予一个ID引用,通过this.$refs.refName来访问元素或子组件的实例
    ```js
    <p ref="p">Hello</p>
    <children ref="children"></children>
    this.$refs.p
    this.$refs.children
    ```