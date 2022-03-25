node {

    def projectImage

    try{

        stage('Checkout') {

                checkout scm

                def nameRegex = scm.userRemoteConfigs.url[0] =~ /^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$/;
                NAME = nameRegex[0][5]

        }

        stage('Load Configuration') {

            sh "echo branch name: ${env.BRANCH_NAME}"

            // build prod stage if is git TAG
            if (env.TAG_NAME){
                BUILD_ENV = 'prod'
            }else{
                BUILD_ENV = env.BRANCH_NAME
            }

            sendSMS("JENKINS - $NAME:build[${env.BUILD_ID}][$BUILD_ENV] INICIOU", "${env.AWS_DEFAULT_REGION}", "${env.AWS_SNS_TOPIC}");

            SERVICE_NAME = "$NAME"
            DOCKER_REPO = "${env.AWS_ACCOUNT_ID}.dkr.ecr.${env.AWS_DEFAULT_REGION}.amazonaws.com"
            LAMBDA_FUNCTION = "$SERVICE_NAME"+"_function"
            DOCKER_ECR_LOGIN = sh(returnStdout: true, script: "aws ecr get-login-password --region ${env.AWS_DEFAULT_REGION}").trim()
            BUILD_ID = "${env.BUILD_ID}"
            LAMBDA_TASK_ROOT = "$BUILD_ENV"

            configFileProvider(
                [configFile(fileId: "$BUILD_ENV"+"_envfile", variable: 'JSON_FILE')]) {

                    def jsonObj = readJSON file: "$JSON_FILE";
                    def confNode = jsonObj."$NAME";

                    // Monta a string de configuração da Lambda
                    // variaveis default: BUILD_ID
                    LAMBDA_CONF_STRING = "BUILD_ID=$BUILD_ID,"
                    confNode.each{entry ->
                        LAMBDA_CONF_STRING = LAMBDA_CONF_STRING + "$entry.key=$entry.value,";
                    };

                    STAGE = "${confNode.STAGE}"
                    CLUSTER_URL = "${confNode.CLUSTER_URL}"
            }

        }

        stage('Pre Build') {

            projectImage = docker.build("$SERVICE_NAME:${env.BUILD_ID}")

        }

        stage('Test') {

            //projectImage.inside {
            //    sh 'pytest'
            //}

        }

        stage('Publish'){

            sh "docker login --username AWS --password $DOCKER_ECR_LOGIN $DOCKER_REPO"

            sh "docker tag $SERVICE_NAME:${env.BUILD_ID} $SERVICE_NAME:latest"

            sh "docker tag $SERVICE_NAME:latest $DOCKER_REPO/$SERVICE_NAME:latest"
            sh "docker push $DOCKER_REPO/$SERVICE_NAME:latest"

        }

        stage('Configure Lambda'){
            sh "aws --region=${env.AWS_DEFAULT_REGION} lambda wait function-updated --function-name $LAMBDA_FUNCTION"

            //Update environment variables
            sh "aws --region=${env.AWS_DEFAULT_REGION} lambda update-function-configuration --function-name $LAMBDA_FUNCTION --environment 'Variables={$LAMBDA_CONF_STRING}'"

            sh "aws --region=${env.AWS_DEFAULT_REGION} lambda wait function-updated --function-name $LAMBDA_FUNCTION"
        }


        stage('Update Lambda Image'){

            sh "echo publishing on $BUILD_ENV"

            //Update $LATEST lambda version
            sh "aws --region=${env.AWS_DEFAULT_REGION} lambda update-function-code --function-name $LAMBDA_FUNCTION --image-uri $DOCKER_REPO/$SERVICE_NAME:latest"

            sh "aws --region=${env.AWS_DEFAULT_REGION} lambda wait function-updated --function-name $LAMBDA_FUNCTION"

            def lambda_return = sh(returnStdout: true, script: "aws lambda publish-version --function-name $LAMBDA_FUNCTION --description build_${env.BUILD_ID}_$BUILD_ENV").trim()

            def lambdaJson = readJSON text: lambda_return

            def newVersion = lambdaJson.Version

            sh "aws --region=${env.AWS_DEFAULT_REGION} lambda update-alias --function-name $LAMBDA_FUNCTION --name $BUILD_ENV --function-version "+newVersion

        }

        stage('Clear'){
            sh "docker rmi $SERVICE_NAME:${env.BUILD_ID}"
            sh "docker rmi $DOCKER_REPO/$SERVICE_NAME:latest"

        }

        stage('Heath Check'){

            sh "curl -sf '$CLUSTER_URL/$STAGE/$SERVICE_NAME/health' >/dev/null"

        }

        sendSMS("JENKINS - $NAME:build[${env.BUILD_ID}][$BUILD_ENV] SUCESSO", "${env.AWS_DEFAULT_REGION}", "${env.AWS_SNS_TOPIC}");


    } catch (e) {

        sendSMS("JENKINS - $NAME:build[${env.BUILD_ID}][$BUILD_ENV] FALHOU: ${env.BUILD_URL}", "${env.AWS_DEFAULT_REGION}", "${env.AWS_SNS_TOPIC}");

        error e

    }

}

def sendSMS(message, region, topic){

    try{
        TELEGRAM_CMD = env.TELEGRAM_SEND_MESSAGE_CMD.replace('<BOT_TOKEN>', env.BOT_TOKEN).replace('<GROUP_ID>', env.GROUP_ID).replace('<MESSAGE>', message)
        sh(returnStdout: true, script: "${TELEGRAM_CMD}")
    } catch(e){
        sh "echo 'Não enviou a notificacao'"
    }

};
