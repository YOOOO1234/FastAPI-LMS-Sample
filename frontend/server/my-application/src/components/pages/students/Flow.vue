<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <v-subheader :class="['text-h5']">{{flow.title}}</v-subheader>
        <v-responsive >
          <v-container class="pa-0">
            <div :class="`rounded-lg`" class="grey lighten-3" v-if="this.flow_sessions.length > 0">
              <v-container class="pa-1">
                <v-row no-gutters>
                  <v-col cols="1" class="text-center">
                    #
                  </v-col>
                  <v-col cols="3" class="text-center">
                    開始時刻
                  </v-col>
                  <v-col cols="3" class="text-center">
                    終了時刻
                  </v-col>
                  <v-col cols="2" class="text-center">
                    テストに回答済み
                  </v-col>
                  <v-col cols="2" class="text-center">
                    成績
                  </v-col>
                  <v-col cols="1" class="text-center">
                    再スタート
                  </v-col>
                </v-row>
                <v-row v-for="(flow_session,i) in this.flow_sessions" :key="flow_session.id" class="pa-0 ma-0" no-gutters>
                  <v-col cols="1" class="text-center">
                    {{i+1}}
                  </v-col>
                  <v-col cols="3" class="text-center">
                    {{flow_session.start_date_time}}
                  </v-col>
                  <v-col cols="3" v-if="flow_session.finish_date_time" class="text-center">
                    {{flow_session.finish_date_time}}
                  </v-col>
                  <v-col cols="3" v-else class="text-center">
                    null
                  </v-col>
                  <v-col cols="2" class="text-center">
                    {{flow_session.is_finished}}
                  </v-col>
                  <v-col cols="2" class="text-center">
                    {{flow_session.flow_session_grade.toFixed(1)}}%
                  </v-col>
                  <v-col cols="1" class="text-center pa-1" >
                    <v-btn @click="restart_flow_session(flow_session.id)" small>
                      start
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </div>
          </v-container>
        </v-responsive>
        <v-container class="mt-6">
          <v-row>
            <div v-html="markdownToHtml(welcome_page_content)"></div>
          </v-row>
          <v-row class="mt-8">
            <v-btn depressed color="primary" @click="start_new_flow_session()">
              演習問題を開始
            </v-btn>
          </v-row>
          <v-row class="mt-8">
            <v-btn depressed color="primary" @click="go_to_course()">
              学習コースにもどる
            </v-btn>
          </v-row>
        </v-container>
      </v-container>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios";
import { marked } from 'marked';

export default {
  name: "Flow",
  props: {
    course_id: Number,
    flow_id: Number
  },
  created: function() {
    let self = this
    axios.get("http://localhost:8000/home_profile", {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.username = response.data.username
          self.is_creater = response.data.create
          axios.get(`http://localhost:8000/get_flow/${self.flow_id}`, {withCredentials: true})
          .then(function(response){
            console.log(response.data)
            self.flow = response.data
          }).catch(
            function(error){
              console.log(error.response)
            }
          )
          axios.get(`http://localhost:8000/get_flow_welcome_page/${self.flow_id}`, {withCredentials: true})
          .then(function(response){
            console.log(response.data)
            self.welcome_page_content = response.data.content
          }).catch(
            function(error){
              console.log(error.response)
            }
          )
          axios.get(`http://localhost:8000/get_flow_sessions/${self.flow_id}`, {withCredentials: true})
          .then(function(response){
            console.log(response.data)
            self.flow_sessions = response.data
          }).catch(
            function(error){
              console.log(error.response)
            }
          )
          axios.get(`http://localhost:8000/get_course/${self.course_id}`, {withCredentials: true})
          .then(function(response){
            console.log(response.data)
            self.course = response.data
          }).catch(
            function(error){
              console.log(error.response)
            }
          )
        }).catch(
          function(error)  {
            if(error.response.status == 401){
              self.$router.push({name:'Signup'})
            }else{
              console.log(error.response)
            }
          }
        )
  },
  data: () => ({
    flow: {},
    welcome_page_content: "",
    username : "",
    is_creater : false,
    markdown:  "# Hello World",
    flow_sessions: [],
    course: {}
  }),
  methods:{
      markdownToHtml(md){
        return marked(md);
      },
      start_new_flow_session(){
        const params = {"flow_id":this.flow_id}
        const config = {
          headers: {
            'Content-Type': 'application/json'
          },
          withCredentials: true
        };
        let self = this
        axios.post(`http://localhost:8000/start_new_flow_session`, params, config)
          .then(function(response){
            console.log(response.data)
            if(response.data.start_success){
              self.$router.push({name:'FlowSession', params: {flow_session_id: response.data.flow_session_id, page_num: 1}})
            }
          }).catch(
            function(error){
              console.log(error)
            }
          )
      },
      go_to_course(){
        this.$router.push({name:'Course', params: {course_id:this.course_id}})
      },
      restart_flow_session(flow_session_id){
        this.$router.push({name:'FlowSession', params: {flow_session_id: flow_session_id, page_num: 1}})
      }
  },
};
</script>
