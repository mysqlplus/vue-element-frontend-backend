<template>
  <div v-if="!item.hidden&&item.children&&hasshowParent(item.children,item)" class="menu-wrapper">

    <template
      v-if="hasOneShowingChild(item.children,item) && (!onlyOneChild.children||onlyOneChild.noShowingChildren)&&!item.alwaysShow">
      <app-link :to="resolvePath(onlyOneChild.path)">
        <el-menu-item :index="resolvePath(onlyOneChild.path)" :class="{'submenu-title-noDropdown':!isNest}">
          <item v-if="onlyOneChild.meta" :icon="onlyOneChild.meta.icon||item.meta.icon"
                :title="generateTitle(onlyOneChild.meta.title)"/>
        </el-menu-item>
      </app-link>
    </template>

    <el-submenu v-else ref="submenu" :index="resolvePath(item.path)">
      <template slot="title">
        <item v-if="item.meta" :icon="item.meta.icon" :title="generateTitle(item.meta.title)"/>
      </template>

      <template v-for="child in item.children" v-if="!child.hidden">
        <sidebar-item
          v-if="child.children&&child.children.length>0"
          :is-nest="true"
          :item="child"
          :key="child.path"
          :base-path="resolvePath(child.path)"
          class="nest-menu"/>

        <app-link v-else :to="resolvePath(child.path)" :key="child.name">
          <el-menu-item :index="resolvePath(child.path)">
            <item v-if="child.meta" :icon="child.meta.icon" :title="generateTitle(child.meta.title)"/>
          </el-menu-item>
        </app-link>
      </template>
    </el-submenu>

  </div>
</template>

<script>
  import path from 'path'
  import {generateTitle} from '@/utils/i18n'
  import {isExternal, parseURL} from '@/utils'
  import Item from './Item'
  import AppLink from './Link'
  import FixiOSBug from './FixiOSBug'

  export default {
    name: 'SidebarItem',
    components: {Item, AppLink},
    mixins: [FixiOSBug],
    props: {
      // route object
      item: {
        type: Object,
        required: true
      },
      isNest: {
        type: Boolean,
        default: false
      },
      basePath: {
        type: String,
        default: ''
      }
    },
    data() {
      return {
        onlyOneChild: null
      }
    },
    methods: {
      hasshowParent(children, parent) {
        var grandpa = ""
        if (parent.hasOwnProperty("parent")) {
          grandpa = parent.parent
        }
        const showingChildren = children.filter(item => {
          var urls = this.$store.getters.urls
          var j = 0
          var flag = false
          var prefix = "/api/v1"
          if (parent.path + "/" + item.path == '/dashboard') {
            flag = true;
          } else {
            for (; j < urls.length; j++) {
              var re = new RegExp(urls[j])
              if (re.test(prefix + grandpa + parent.path + "/" + item.path + "/")) {
                flag = true
              }
            }
          }
          if (item.hidden || !flag || (item.meta.roles != undefined && !this.$store.getters.roles.some(role => item.meta.roles.indexOf(role) >= 0))) {
            return false
          } else {
            return true
          }
        })

        if (showingChildren.length >= 1) {
          return true
        }
        // Show parent if there are no child router to display
        if (showingChildren.length === 0) {
          return false
        }
        return false
      },

      hasOneShowingChild(children, parent) {
        var grandpa = ""
        if (parent.hasOwnProperty("parent")) {
          grandpa = parent.parent
        }
        const showingChildren = children.filter(item => {
          var urls = this.$store.getters.urls
          var j = 0
          var flag = false
          var prefix = "/api/v1"
          if (parent.path + "/" + item.path == '/dashboard') {
            flag = true;
          } else {
            for (; j < urls.length; j++) {
              var re = new RegExp(urls[j])
              if (re.test(prefix + grandpa + parent.path + "/" + item.path + "/")) {
                flag = true
              }
            }
          }

          if (item.hidden || !flag || (item.meta.roles != undefined && !this.$store.getters.roles.some(role => item.meta.roles.indexOf(role) >= 0))) {
            item.hidden = true
            return false
          } else {
            if (parent.path + "/" + item.path == '/dashboard') {
              this.onlyOneChild = item
            }
            return true
          }
        })

        // When there is only one child router, the child router is displayed by default
        if (parent.meta == null && showingChildren.length === 1) {
          return true
        }
        // Show parent if there are no child router to display
        if (showingChildren.length === 0) {
          // this.onlyOneChild = {...parent, path: '', noShowingChildren: true}
          parent.hidden = true;
          return false
        }

        return false
      },
      resolvePath(routePath) {
        if (this.isExternalLink(routePath)) {
          return routePath
        }
        return path.resolve(this.basePath, routePath)
      },
      isExternalLink(routePath) {
        return isExternal(routePath)
      },
      generateTitle
    }
  }
</script>
