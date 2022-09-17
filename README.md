
## Contents of this markdown summary:
  
- [Headings](#heading-1--text)
- [Code highlighting](#code-snippet)
- [Blockquote](#blockquote)
- [Links](#links)
  - [Links to a document sections](#links-to-a-document-sections)
  - [Link reference (shortcut)](#nerdy-stuff-with-links----reference-or-a-shortcut-for-multiple-link-usage-in-a-document-----)
  - [Images](#images)
- [Text formatting](#text-formatting)
  - [Horizontal separator](#horizontal-separator--or-___)
  - [Line break](#line-break)
- [Lists](#lists)
  - [Ordered](#ordered)
  - [List with checkboxes](#list-with-checkboxes)
- [Table](#table)
- [Toggle (dropdown)](#toggle-dropdown)

  <br>  <br>

# Heading 1: `# text`
## Heading 2: `## text`
Just like in HTML, headings are from h1 up to h6.
  <br>


## Code:
- To highlight only a part of a sentence `as a code`, put it within a pair of single backticks ( ` ):
```
`code`
```
- To have fenced multiline code, like below, put it between two lines of triple backticks ` ``` `.
```js 
let numbers = [0, 1, 10, 2, 20, 3, 30];
numbers.sort((a,b) => a - b);
console.log(numbers);
//[0, 1, 2, 3, 10, 20, 30]
```
In the first line of two, straight after the backticks we can define a language of code to put its highlighting, 
like this: ` ```js `
  <br>  <br>

## Blockquote

> Starting a line with gt sign `>`   <br>we have such a highlight.
>> Even nesting is possible, augmenting gt `>>`.

  <br> 

## Links 

To put a [link](https://me.me/i/microsoft-excel-bill-gates-says-ur-mom-gay-lol-%D0%BE%D0%BA-866d10ba370a4820bacb2ad62a50c389 "text to see on mouse hover") within a text, use this syntax:
```
[text](link "text to see on mouse hover")
```
  <br>

## Links to a document sections

I can address you to the previous part of this page, using this [link](#links "The previous section"):
```
[link](#heading-from-this-document "text on mouse hover")
```
  <br>

## Nerdy stuff with links:   <br> Reference or a shortcut for multiple link usage in a document   <br>  <br>

Firstly we define a shortcut once:
```
[shortcut]: link "text to see on mouse hover"
```
And then we can use this handy shortcut this way:
```
[text of a link][shortcut]
```
(Note that the second pair of braces is square too)
  <br>  <br>

Let's look at multiple shortcut usage on the example:
```
// shortcut creation
[yt]: youtube.com "main page of YouTube"

// fast shortcut usage
[First YouTube mention][yt]
[Second][yt]
[Third][yt]
```
And that's what we get from code above:

[yt]: youtube.com "main page of YouTube"

[First YouTube mention][yt]  <br>
[Second][yt]  <br>
[Third][yt]



  <br>  <br>

## Images

To paste an image with alt text:
```
![alt text](link to an image)
```
And to make a link from a whole image, we recurse the previous structure:
```
[ ![alt text](link to an image) ] (link)
```
  <br>  <br>

# Text formatting

*Italic*:
```
*text* or _text_
```
**Bold**:
```
**text** or __text__
```
***Bold and italic***:
```
***text*** or ___text___
```
~~Strikethrough~~:
```
~~text~~
```
  <br>

## Horizontal separator: `***` or `___`
  <br>

Text above three asterisks/underscores
___
Text below three asterisks/underscores
  <br>  <br>

## Line break
To add a line break:
- Two "enter"s instead of one;
- HTML break, but with two spaces before:
```
_ _ <br>
```
  <br>  <br>

# Lists

## Ordered

This list renders number of a bullet by itself, I even can put "1." before every bullet, order in a document anyway shall be correct:
1. Bullet №1
1. Bullet №2
1. Bullet №3
1. Bullet №4
1. Bullet №5

(But it works only starting at 1)
  <br>  <br>

## List with checkboxes ##
Syntax:
```
- [x] List syntax is required
- [x] This item is complete
- [ ] This one isn't complete
```
That's how it looks:
- [x] List syntax is required
- [x] This item is complete
- [ ] This one isn't complete
  <br>  <br>  <br>


# Table

- Vertical pipes `|` separate columns;  <br>
- Horizontal triple hyphens `---` separate headings from table contents;
- Colons around triple hyphen define alignment of a column:  <br> left `:---`, center `:---:`, right `---:`.
```
| Packages |     Description      | Version |
| :---     |         :---:        |    ---: |
| React    | Javascript framework |    v18.0|
| Next.js  |    React framework   |    v12.0|
```
That's what we have:

| Packages |      Description     | Version |
| :---     |         :---:        |    ---: |
| React    | Javascript framework |    v18.0|
| Next.js  |    React framework   |    v12.0|

(Spaces, tabulation in code may be messy, rendering still shall be correct)

  <br>  <br>

## Toggle (dropdown)

We can use some (mb all) HTML tags in markdown, just like toggle:
<details>
  <summary>Our cool toggle</summary>
  Some info inside of that toggle.
</details>

Which is:
```
<details>
  <summary>Our cool toggle</summary>
  Some info inside of that toggle.
</details>
```



