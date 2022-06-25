variable "first_bucket" {
  default = "poc-input-bucket-sandy"
  type    = string
}

variable "second_bucket" {
  default = "poc-output-bucket-sandy"
}

variable "storage_class" {

}

variable "environment" {
  default = "POC_ENV"
}

variable "author" {
  default = "Sandeep Sharma"
}