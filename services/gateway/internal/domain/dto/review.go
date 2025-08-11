package dto

type ReviewRequestDTO struct {
	TaskID         string `json:"task_id" binding:"required"`
	RepositoryLink string `json:"repository_link" binding:"required"`
}

type ReviewResponseDTO struct {
	TaskID         string `json:"task_id"`
	Rating         string `json:"rating"`
	RepositoryLink string `json:"repository_link"`
}
