<template>
<mu-dialog :open="state.dialog.userManage" :title="`对用户 ${user.nickname} 进行管理操作`" @close="close" scrollable>
    <div class="topic-manage-item" style="margin-top: 30px;">
        <span class="label">ID</span>
        <div class="right">{{user.id}}</div>
    </div>
    <div class="topic-manage-item">
        <span class="label">Email</span>
        <div class="right">
            <div>{{user.email}}</div>
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">昵称</span>
        <div class="right">
            <div>{{user.nickname}}</div>
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">注册时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.time" />
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">最后登录时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.key_time" />
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">简介</span>
        <div class="right">
            <mu-text-field v-model="user.biology" :maxLength="255"/>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">状态</span>
        <div class="right" style="display: flex">
            <mu-radio name="state" :label="i" :nativeValue="j.toString()" v-model="user.state" v-for="i, j in state.misc.POST_STATE_TXT" :key="j" class="demo-radio"/>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">用户组</span>
        <div class="right" style="display: flex">
            <mu-radio name="group" :label="i" :nativeValue="j.toString()" v-model="user.group" v-for="i, j in state.misc.USER_GROUP_TXT" :key="j" class="demo-radio"/>
        </div>
    </div>

    <mu-flat-button slot="actions" @click="close" primary label="取消"/>
    <mu-flat-button slot="actions" primary @click="ok" label="确定"/>
</mu-dialog>
</template>

<style>
.no-left-padding {
    padding-left: 0;
    margin-left: 0;
}
</style>


<style scoped>
.topic-manage-item {
    display: flex;
    align-items: baseline;
    min-height: 56px;
}

.topic-manage-item > .label {
    flex: 1 0 0;
}

.topic-manage-item > .right {
    flex: 4 0 0;
}

.demo-radio {
    margin-right: 15px;
}

.demo-slider {
    margin-bottom: 0;
}

.hl {
    color: red
}
</style>

<script>
import state from '@/state.js'
import api from '@/netapi.js'

export default {
    data () {
        return {
            state,
            user: {name: ''},
            save: {}
        }
    },
    methods: {
        ok: async function () {
            let data = $.objDiff(this.user, this.save)
            if (data.state) data.state = Number(data.state)
            if (data.group) data.group = Number(data.group)

            let ret = await api.user.set({id: this.user.id}, data, 'admin')
            if (ret.code === 0) {
                if (state.dialog.userManageData) {
                    _.assign(state.dialog.userManageData, data)
                }
                $.message_success('用户信息设置成功')
            } else $.message_by_code(ret.code)

            state.dialog.userManage = null
        },
        close () {
            state.dialog.userManage = null
        }
    },
    watch: {
        'state.dialog.userManage': async function (val) {
            if (val) {
                let info = await api.user.get({id: state.dialog.userManageData.id}, 'admin')
                if (info.code === api.retcode.SUCCESS) {
                    this.user = info.data
                    this.user.state = this.user.state.toString()
                    this.user.group = this.user.group.toString()
                    this.save = _.clone(this.user)
                } else {
                    $.message_by_code(info.code)
                }
            }
        }
    }
}
</script>
