<template>
  <v-container>
    <v-responsive :max-width="1200" class="mx-auto">
      <v-container>
        <v-row>
          <v-col cols="6">
            <v-subheader :class="['text-h5']">{{course.course_name}}</v-subheader>
          </v-col>
          <v-col cols="6">
            <v-container>  
              <v-row justify="end">
                <div>
                  {{this.user_info.username}} ( {{this.user_info.email}})<br>
                  {{this.user_info.kind_name}} としてログイン中
                </div>
              </v-row>
              <v-row justify="end">
                <v-btn text color="red" @click="logout()" value="POST">ログアウト</v-btn>
              </v-row>
            </v-container>
          </v-col>
        </v-row>
        <v-row>
        <v-col cols="2">
          <v-btn @click="move_to_course_info()" depressed block color="transparent"  class="mb-2"> 
            コース情報
          </v-btn>
        </v-col>
        <v-col cols="2">
          <v-btn @click="move_to_course_taking()" depressed block color="transparent"  class="mb-2">
            履修者
          </v-btn>
          <v-divider class="red"></v-divider>
        </v-col >  
        <v-col cols="2">
          <v-btn @click="move_to_course_preview()" depressed block color="transparent"  class="mb-2">
            プレビュー
          </v-btn>
        </v-col >  
        <v-col cols="2">
          <v-btn @click="move_to_course_edit()" depressed block color="transparent"  class="mb-2">
            編集
          </v-btn>
        </v-col>  
        </v-row>
        <v-divider class="mt-0"></v-divider>
        <v-row class="mt-5" >
          <v-responsive :max-width="1000" class="mx-auto">
            <v-container>
              <v-row>
                <v-col>
                  <v-subheader :class="['text-h5']">履修中のユーザ</v-subheader>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-data-table
                    :headers="headers"
                    :items="taking_students"
                    :items-per-page="5"
                    :search="search"
                    
                  ></v-data-table>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-subheader :class="['text-h5']">履修者の追加</v-subheader>
                </v-col>
              </v-row>
              <v-row >
                <v-col cols="5">
                  <v-text-field v-model="add_email" label="Emailアドレスを入力" outlined dense></v-text-field>
                </v-col>
                <v-col cols="1">
                  <v-btn @click="add_taking_students()" color="primary">追加</v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-responsive>
        </v-row>
        
      </v-container>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",
  props: {
    course_id: Number
  },
  created: function() {
    this.get_home_profile()
  },
  data: () => ({
    
    headers: [
      {text: "ユーザ名", value:"username"},
      {text: "Email", value:"email"},
      {text: "アクティブ", value:"is_active"},
      {text: "種別", value:"kind_name"}
    ],
    user_info : {},
    is_create : false,
    course: {},
    taking_students: [],
    add_email: "",
    add_user_error: ""
  }),
  methods:{
    logout: function(){
      try{
        const res = axios.post("http://localhost:8000/logout",{},{withCredentials: true})
        console.log(res.data)
        this.moveToLogin()
      }catch(error){
        const {status,statusText} = error.response;
        if(status == 401)
          this.moveToLogin()
        console.log(status,statusText)
      }
    },
    moveToLogin: function(){
      this.$router.push({name:'Login'})
    },
    move_to_course_info(){
      this.$router.push({name:'CourseInfo', params:{"course_id":this.course_id}})
    },
    move_to_course_taking(){
      this.$router.push({name:'CourseTaking',params:{"course_id":this.course_id}})
    },
    move_to_course_preview(){
      this.$router.push({name:'CoursePreview',params:{"course_id":this.course_id}})
    },
    move_to_course_edit(){
      this.$router.push({name:'CourseEdit',params:{"course_id":this.course_id}})
    },
    get_home_profile(){
      let self = this
      axios.get("http://localhost:8000/home_profile", {withCredentials: true})
      .then(function(response){
        console.log(response.data)
        self.user_info = response.data
        self.is_creater = response.data.create
        if(self.is_creater){
          self.get_course_info()
          self.get_taking_students()
        }
      }).catch(
        function(error)  {
          console.log(error)
          if(error.response.status == 401){
            self.$router.push({name:'Signup'})
          }else{
            console.log(error.response)
          }
        }
      )
    },
    get_course_info(){
      let self = this
      axios.get(`http://localhost:8000/get_course_info/${self.course_id}`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.course = response.data
        }).catch(function(error){
          console.log(error.response)
        }).catch(function(error)  {
          if(error.response.status == 401){
            self.$router.push({name:'Signup'})
          }else{
            console.log(error.response)
          }
        }
      ) 
    },
    get_taking_students(){
      let self = this
      axios.get(`http://localhost:8000/get_taking_students/${self.course_id}`, {withCredentials: true})
        .then(function(response){
          console.log(response.data)
          self.taking_students = response.data
        }).catch(function(error){
          console.log(error.response)
        }).catch(function(error)  {
          if(error.response.status == 401){
            self.$router.push({name:'Signup'})
          }else{
            console.log(error.response)
          }
        }
      ) 
    },
    add_taking_students(){
      const params = {"course_id":this.course_id, "email": this.add_email}
      console.log(JSON.stringify(params));
      const config = {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      };
      let self = this
      axios.post('http://localhost:8000/register_taking_student', params, config)
      .then(function(response){
        console.log(response.data)
        self.get_taking_students()
      })
    }
  },
};
</script>
