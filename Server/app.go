package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
)

type Post struct {
	ID     int    `json:"id"`
	Title  string `json:"title"`
	Author string `json:"author"`
}

type Comment struct {
	ID     int    `json:"id"`
	Body   string `json:"body"`
	PostID int    `json:"postID"`
}

type Profile struct {
	Name string `json:"name"`
}

var posts []Post
var comments []Comment
var profile Profile

// StartMain Garoutin
func main() {
	logfile, err := os.OpenFile("Logs/server.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	defer logfile.Close()

	multiWriter := io.MultiWriter(os.Stdout, logfile)
	log.SetOutput(io.MultiWriter(os.Stdout, logfile))

	//New router
	router := mux.NewRouter()

	//MultiWriter
	router.Use(func(next http.Handler) http.Handler {
		return handlers.LoggingHandler(multiWriter, next)
	})

	// Endpoints for post
	router.HandleFunc("/posts", GetPosts).Methods("GET")
	router.HandleFunc("/posts/{id}/comments", GetPostComments).Methods("GET")
	router.HandleFunc("/posts/author/{author}", GetAuthorPosts).Methods("GET")
	router.HandleFunc("/posts", CreatePost).Methods("POST")
	router.HandleFunc("/posts/{id}", GetPost).Methods("GET")
	router.HandleFunc("/posts/{id}", UpdatePost).Methods("PUT")
	router.HandleFunc("/posts/{id}", DeletePost).Methods("DELETE")

	//Endpoints for comments
	router.HandleFunc("/comments", GetComments).Methods("GET")
	router.HandleFunc("/comments/post/{postID}", GetCommentsPost).Methods("GET")
	router.HandleFunc("/comments", CreateComment).Methods("POST")
	router.HandleFunc("/comments/{id}", GetComment).Methods("GET")
	router.HandleFunc("/comments/{id}", UpdateComment).Methods("PUT")
	router.HandleFunc("/comments/post/{postID}", DeletePostComments).Methods("DELETE")
	router.HandleFunc("/comments/{id}", DeleteComment).Methods("DELETE")

	//Endpoints for profile
	router.HandleFunc("/profile", GetProfile).Methods("GET")
	router.HandleFunc("/profile", CreateProfile).Methods("POST")
	router.HandleFunc("/profile", UpdateProfile).Methods("PUT")
	router.HandleFunc("/profile", DeleteProfile).Methods("DELETE")

	// Set up a signal handler to catch termination signals
	stopChan := make(chan os.Signal, 1)
	signal.Notify(stopChan, os.Interrupt, syscall.SIGTERM)

	// Start server garoutine
	go func() {
		log.Printf("Server is running on :5050")
		log.Fatal(http.ListenAndServe(":5050", router))
	}()

	// Wait for a signal shut down the server
	<-stopChan
	log.Println("Shutting down the server...")

	saveDataToJSON()

	log.Println("Server has been shut down.")
}

//EndMain Garoutin

func saveDataToJSON() {
	file, err := os.Create("DataBase/db.json")
	if err != nil {
		log.Println("Error creating or opening db.json file:", err)
		return
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "    ")

	err = encoder.Encode(map[string]interface{}{
		"posts":    posts,
		"comments": comments,
		"profile":  profile,
	})
	if err != nil {
		log.Println("Error encoding data to JSON:", err)
	}
}

// Handlers for posts
func GetPosts(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(posts)
	saveDataToJSON()
}

func CreatePost(w http.ResponseWriter, r *http.Request) {
	var post Post
	_ = json.NewDecoder(r.Body).Decode(&post)
	post.ID = len(posts) + 1
	posts = append(posts, post)
	json.NewEncoder(w).Encode(post)
	saveDataToJSON()
}

func GetPost(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id, _ := strconv.Atoi(params["id"])

	for _, item := range posts {
		if item.ID == id {
			json.NewEncoder(w).Encode(item)
			saveDataToJSON()
			return
		}
	}

	json.NewEncoder(w).Encode(&Post{})
}

func UpdatePost(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id, _ := strconv.Atoi(params["id"])

	var updatedPost Post
	_ = json.NewDecoder(r.Body).Decode(&updatedPost)

	for index, item := range posts {
		if item.ID == id {
			posts[index] = updatedPost
			json.NewEncoder(w).Encode(updatedPost)
			saveDataToJSON()
			return
		}
	}

	json.NewEncoder(w).Encode(&Post{})
}

func DeletePost(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id, _ := strconv.Atoi(params["id"])

	for index, item := range posts {
		if item.ID == id {
			posts = append(posts[:index], posts[index+1:]...)
			break
		}
	}

	json.NewEncoder(w).Encode(posts)
	saveDataToJSON()
}

func GetAuthorPosts(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	author := params["author"]

	authorPosts := []Post{}
	for _, post := range posts {
		if post.Author == author {
			authorPosts = append(authorPosts, post)
		}
	}

	json.NewEncoder(w).Encode(authorPosts)
	saveDataToJSON()
}

func GetPostComments(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	postID, _ := strconv.Atoi(params["postID"])

	postComments := []Comment{}
	for _, comment := range comments {
		if comment.PostID == postID {
			postComments = append(postComments, comment)
		}
	}

	json.NewEncoder(w).Encode(postComments)
	saveDataToJSON()
}

func DeletePostComments(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	postID, _ := strconv.Atoi(params["postID"])

	commentsToDelete := []Comment{}
	for index, comment := range comments {
		if comment.PostID == postID {
			commentsToDelete = append(commentsToDelete, comment)
			comments = append(comments[:index], comments[index+1:]...)
		}
	}

	json.NewEncoder(w).Encode(commentsToDelete)
	saveDataToJSON()
}

// Handlers for comments
func GetComments(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(comments)
}

func CreateComment(w http.ResponseWriter, r *http.Request) {
	var comment Comment
	_ = json.NewDecoder(r.Body).Decode(&comment)
	comment.ID = len(comments) + 1
	comments = append(comments, comment)
	json.NewEncoder(w).Encode(comment)
	saveDataToJSON()
}

func GetComment(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id, _ := strconv.Atoi(params["id"])

	for _, item := range comments {
		if item.ID == id {
			json.NewEncoder(w).Encode(item)
			saveDataToJSON()
			return
		}
	}

	json.NewEncoder(w).Encode(&Comment{})
}

func UpdateComment(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id, _ := strconv.Atoi(params["id"])

	var updatedComment Comment
	_ = json.NewDecoder(r.Body).Decode(&updatedComment)

	for index, item := range comments {
		if item.ID == id {
			comments[index] = updatedComment
			json.NewEncoder(w).Encode(updatedComment)
			saveDataToJSON()
			return
		}
	}

	json.NewEncoder(w).Encode(&Comment{})
}

func DeleteComment(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id, _ := strconv.Atoi(params["id"])

	for index, item := range comments {
		if item.ID == id {
			comments = append(comments[:index], comments[index+1:]...)
			break
		}
	}

	json.NewEncoder(w).Encode(comments)
	saveDataToJSON()
}

func GetCommentsPost(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	postID, _ := strconv.Atoi(params["id"])

	postComments := []Comment{}
	for _, comment := range comments {
		if comment.PostID == postID {
			postComments = append(postComments, comment)
		}
	}

	json.NewEncoder(w).Encode(postComments)
	saveDataToJSON()
}

// Handlers for profile
func GetProfile(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(profile)
	saveDataToJSON()
}

func CreateProfile(w http.ResponseWriter, r *http.Request) {
	var newProfile Profile
	_ = json.NewDecoder(r.Body).Decode(&newProfile)
	profile = newProfile
	json.NewEncoder(w).Encode(newProfile)
	saveDataToJSON()
}

func UpdateProfile(w http.ResponseWriter, r *http.Request) {
	var updatedProfile Profile
	_ = json.NewDecoder(r.Body).Decode(&updatedProfile)
	profile = updatedProfile
	json.NewEncoder(w).Encode(updatedProfile)
	saveDataToJSON()
}

func DeleteProfile(w http.ResponseWriter, r *http.Request) {
	profile = Profile{}
	json.NewEncoder(w).Encode(profile)
	saveDataToJSON()
}
