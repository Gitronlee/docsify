# vue项目开发笔记

需要先安装nodejs和vue-cli（脚手架）

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
   
   解决方法为：`软件和更新` 勾选 `可从互联网下载 Canonical 支持的免费和开源软件(main) `和 `社区维护的免费和开源软件(universe) `
   执行 ``sudo apt-get update``
3. 更换淘宝的镜像
   `sudo npm config set registry https://registry.npm.taobao.org`
4. 安装更新版本的工具N，执行：
   `sudo npm install n -g`
5. 更新新node版本，执行：
   `sudo n stable`
6. 安装 cnpm `sudo npm install cnpm -g`

## 二、安装vue-cli

使用cnpm安装 `sudo cnpm install vue-cli -g`(vue cli 2)
`npm install -g @vue/cli`(vue cli3 我用的vue3)

## 三、创建vue-web项目

### 1. 一键构建目录结构

`vue create project-vue3`此处我选择的是 vue2.x
一路回车固然简单，但是最好将各种lint test项先no之，避免起步的各种报错~

### 2. 阻止显示生产模式的消息

生产模式：`npm run build` 打包之后给后端放在服务端上用的`Vue.config.productionTip = false`
的意思是阻止显示生产模式的消息。

### 3. new Vue 和 store

一个 Vue 应用由一个通过 new Vue 创建的根 Vue 实例，以及可选的嵌套的、可复用的组件树组成。当一个 Vue 实例被创建时，它将 data 对象中的所有的属性加入到 Vue 的响应式系统中。

```js
new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
```

`render: h => h(App)` 是下面内容的缩写：

```
render: function (createElement) {
    return createElement(App);
}
```

每一个 Vuex 应用的核心就是 store（仓库）。“store”基本上就是一个容器，它包含着你的应用中大部分的**状态 (state)** 。

2. 在项目运行中，main.js作为项目的入口文件，运行中，找到其实例需要挂载的位置，即index.html中，刚开始，index.html的挂载点处的内容会被显示，但是随后就被实例中的组件中的模板中的内容所取代，所以我们会看到有那么一瞬间会显示出index.html中正文的内容。

而index.html中的Title部分不会被取代，所以会一直保留。
### export default 和 export ：

1.export与export default均可用于导出常量、函数、文件、模块等

2.可以在其它文件或模块中通过import+(常量 | 函数 | 文件 | 模块)名的方式，将其导入，以便能够对其进行使用

3.在一个文件或模块中，export、import可以有多个，export default仅有一个

4.通过export方式导出，在导入时要加{ }，export default则不需要

### 安装cnpm
安装命令为`sudo npm install cnpm -g --registry=https://registry.npmmirror.com`

## 使用并安装必要的组件

ant-design-vue
```
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
```
js-cookie
```
import Cookies from 'js-cookie'
```
```
import VueContextMenu from 'vue-contextmenu'
```

安装命令分别为
`cnpm install ant-design-vue --save`
`cnpm install js-cookie --save`
`cnpm install --save vue-contextmenu`

### 安装依赖

`sudo npm install`

### 安装SASS加速器

`sudo cnpm install sass-loader node-sass --save-dev`

### 启动测试

`npm run dev`

